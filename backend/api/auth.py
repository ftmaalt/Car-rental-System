# backend/api/auth.py
from flask import Blueprint, request, jsonify, make_response
from db.init_supabase import get_supabase_client
import os

auth_bp = Blueprint("auth", __name__)
supabase = get_supabase_client()

# Cookies we set for the browser session
COOKIE_ACCESS = "sb-access"
COOKIE_REFRESH = "sb-refresh"
COOKIE_OPTS = dict(httponly=True, secure=False, samesite="Lax")  # set secure=True in production (HTTPS)

FRONTEND_BASE = os.getenv("FRONTEND_BASE", "http://127.0.0.1:5500")

def _ok_with_tokens(payload, session):
    """Return JSON with access/refresh cookies set (if present)."""
    resp = make_response(jsonify(payload))
    if session and getattr(session, "access_token", None):
        resp.set_cookie(COOKIE_ACCESS, session.access_token, max_age=60*60, **COOKIE_OPTS)
    if session and getattr(session, "refresh_token", None):
        resp.set_cookie(COOKIE_REFRESH, session.refresh_token, max_age=60*60*24*7, **COOKIE_OPTS)
    return resp

def _get_access_from_cookies():
    """Try to read access token from cookies; if missing but refresh exists, attempt refresh."""
    tok = request.cookies.get(COOKIE_ACCESS)
    if tok:
        return tok
    ref = request.cookies.get(COOKIE_REFRESH)
    if not ref:
        return None
    try:
        refreshed = supabase.auth.refresh_session(ref)
        if refreshed and refreshed.session and refreshed.session.access_token:
            return refreshed.session.access_token
    except Exception:
        pass
    return None


@auth_bp.post("/auth/signup")
def signup():
    """Create a new user (email/password). If email already exists in our users table,
    return 409 with a friendly message."""
    data = request.get_json(force=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = (data.get("password") or "").strip()
    full_name = (data.get("name") or "").strip()

    if not email or not password:
        return jsonify({"error": "email and password required"}), 400

    # 1) If the email exists in our profiles, treat it as already registered.
    try:
        exists = (
            supabase.table("users")
            .select("id")
            .eq("email", email)
            .limit(1)
            .execute()
            .data
        )
        if exists:
            return jsonify({"error": "This email is already registered. Please sign in."}), 409
    except Exception:
        pass  # if this select fails we still attempt signup

    # 2) Create Auth user
    try:
        res = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {"data": {"name": full_name}}
        })

        if getattr(res, "user", None) is None:
            # Some SDK variants return user=None when email already exists
            return jsonify({"error": "This email is already registered. Please sign in."}), 409

        # 3) Upsert a profile row. If RLS blocks this (running with anon key), ignore —
        #     the first successful login will link auth_uid.
        try:
            supabase.table("users").upsert({
                "auth_uid": res.user.id,
                "email": email,
                "name": full_name or email.split("@")[0],
                "role": "user",
            }).execute()
        except Exception:
            pass

        # 4) If email confirmation is required, session is None -> tell user to check email
        if res.session:
            return _ok_with_tokens(
                {"message": "Account created.", "user": {"email": email, "name": full_name}},
                res.session
            )
        return jsonify({"message": "Check your email to confirm your account."}), 200

    except Exception as e:
        msg = str(e).lower()
        if "already registered" in msg or "duplicate" in msg:
            return jsonify({"error": "This email is already registered. Please sign in."}), 409
        return jsonify({"error": str(e)}), 400


@auth_bp.post("/auth/login")
def login():
    """Authenticate and set cookies; also link auth_uid to the users row if missing."""
    data = request.get_json(force=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = (data.get("password") or "").strip()

    if not email or not password:
        return jsonify({"error": "email and password required"}), 400

    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})

        if not res or not res.user or not res.session:
            return jsonify({"error": "Invalid email or password"}), 401

        # Link auth_uid on first login if there's a seeded profile without it
        try:
            supabase.table("users").update({"auth_uid": res.user.id}) \
                .eq("email", email).is_("auth_uid", None).execute()
        except Exception:
            pass

        name = res.user.user_metadata.get("name") if res.user.user_metadata else email.split("@")[0]
        payload = {"message": "Login successful", "user": {"email": res.user.email, "name": name}}
        return _ok_with_tokens(payload, res.session)

    except Exception as e:
        msg = str(e).lower()
        if "invalid login credentials" in msg or "email not confirmed" in msg:
            return jsonify({"error": "Invalid email or password"}), 401
        return jsonify({"error": str(e)}), 400


@auth_bp.get("/auth/me")
def me():
    """Return the current user profile (by cookie)."""
    tok = _get_access_from_cookies()
    if not tok:
        return jsonify({"user": None})
    try:
        info = supabase.auth.get_user(tok)
        if info and info.user:
            name = info.user.user_metadata.get("name") if info.user.user_metadata else (info.user.email or "").split("@")[0]
            return jsonify({"user": {"email": info.user.email, "name": name}})
    except Exception:
        pass
    return jsonify({"user": None})


@auth_bp.post("/auth/logout")
def logout():
    """Remove cookies; (optional) sign out from Supabase."""
    try:
        supabase.auth.sign_out()
    except Exception:
        pass
    resp = make_response(jsonify({"message": "Logged out"}))
    resp.delete_cookie(COOKIE_ACCESS)
    resp.delete_cookie(COOKIE_REFRESH)
    return resp
