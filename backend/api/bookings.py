from flask import Blueprint, request, jsonify
from db.init_supabase import get_supabase_client

bookings_bp = Blueprint("bookings", __name__)
supabase = get_supabase_client()

def _access_from_cookies(req):
    return req.cookies.get("sb-access") or None

@bookings_bp.post("/bookings")
def create_booking():
    # must be authenticated (cookie is set by /auth/login or /auth/signup)
    if not _access_from_cookies(request):
        return jsonify({"error": "unauthenticated"}), 401

    body = request.get_json(force=True) or {}
    vehicle_id = body.get("vehicle_id")
    start_at   = body.get("start_at")
    end_at     = body.get("end_at")

    if not all([vehicle_id, start_at, end_at]):
        return jsonify({"error": "vehicle_id, start_at, end_at required"}), 400

    # Map auth.uid() -> users.id via RPC
    # Note: Using service key server-side allows RPC call; RLS still applies on table ops
    uid_res = supabase.rpc("current_user_id", {}).execute()
    user_id = uid_res.data
    if not user_id:
        return jsonify({"error": "no linked profile for this auth user"}), 403

    ins = {
        "user_id": user_id,
        "vehicle_id": vehicle_id,
        "start_at": start_at,
        "end_at": end_at,
        "status": "pending"
    }
    created = supabase.table("bookings").insert(ins).select("*").single().execute().data
    return jsonify(created), 201

@bookings_bp.post("/bookings/cancel")
def cancel_booking():
    if not _access_from_cookies(request):
        return jsonify({"error": "unauthenticated"}), 401

    booking_id = (request.get_json(force=True) or {}).get("booking_id")
    if not booking_id:
        return jsonify({"error": "booking_id required"}), 400

    # RLS ensures only owner can update
    res = (supabase.table("bookings")
           .update({"status": "cancelled"})
           .eq("id", booking_id)
           .select("*")
           .single()
           .execute())
    if not res.data:
        return jsonify({"error": "not found or not yours"}), 404
    return jsonify(res.data)
