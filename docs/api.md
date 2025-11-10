# docs/api.md — Auth + “Current User” Display

## Base URL

```
http://127.0.0.1:5000/api
```

All endpoints are JSON. Cookies are used for the session (HTTP‑only).

---

## Auth endpoints

### POST `/auth/signup`

Create a new account and (if email confirmation is enabled) send a verification email.

**Request**

```json
{
  "name": "Eman Alasaadi",
  "email": "eman.alasaadi5@gmail.com",
  "password": "••••••••"
}
```

**Responses**

* `200 OK`

  ```json
  { "message": "Check your email to confirm your account." }
  ```
* `409 Conflict` – account already exists

  ```json
  { "error": "User already exists" }
  ```
* `400/422` – validation or other error

  ```json
  { "error": "…" }
  ```

**Frontend note**

* The app stores `cr_last_email` in `localStorage` after submission so the login page can prefill the email field automatically.

---

### POST `/auth/login`

Authenticate the user. Sets the session cookie.

**Request**

```json
{
  "email": "eman.alasaadi5@gmail.com",
  "password": "••••••••"
}
```

**Responses**

* `200 OK`

  ```json
  {
    "user": {
      "name": "Eman Alasaadi",
      "email": "eman.alasaadi5@gmail.com"
    }
  }
  ```

  Headers include `Set-Cookie: <session>` (HTTP‑only).
* `401 Unauthorized`

  ```json
  { "error": "Invalid email or password" }
  ```

**Frontend behavior**

* On success the app stores:

  * `cr_user_name` = `user.name || user.email`
  * `cr_user_email` = `email`
* Then it redirects to `frontend/index.html`.

---

### GET `/auth/me`

Return the **currently authenticated user** (derived from the session cookie).

**Response**

* `200 OK` (when logged in)

  ```json
  { "user": { "name": "Eman Alasaadi", "email": "eman.alasaadi5@gmail.com" } }
  ```
* `401 Unauthorized` (no valid session)

  ```json
  { "error": "Not authenticated" }
  ```

**Used by**

* The login page (to prefill the email if a session already exists).
* The **Contribute** page to show **only the logged‑in user** (details below).

---

### (Optional) POST `/auth/logout`

If present, clears the session cookie.

**Response**

```json
{ "message": "Logged out" }
```

---

## “Contribute” page: show **only the current user**

The page does **not** list all users. It renders **one card** for the exact person who is signed in.

**Logic**

1. Try `GET /auth/me` with `credentials: "include"` to read `{ user }` from the session.
2. If no session yet, fall back to local cache:

   * `cr_user_name`
   * `cr_user_email` (or `cr_last_email`, set during signup)
3. If neither is available → show “Please sign in to see your account details.”

**Example DOM targets**

```html
<div id="user-list"></div>     <!-- the single card is injected here -->
<p id="no-results" style="display:none"></p>
```

**Rendered card**

```html
<article class="faq-card">
  <h3>Eman Alasaadi</h3>
  <p><a class="email-link" href="mailto:eman.alasaadi5@gmail.com">eman.alasaadi5@gmail.com</a></p>
</article>
```

---

## Frontend integration details

### Login page (`frontend/login.html`)

* Prefills email (priority): `/auth/me` → `?email=…` → `localStorage(cr_user_email | cr_last_email)`.
* On success: stores `cr_user_name`, `cr_user_email`; redirects to `index.html`.

### Signup page (`frontend/signup.html`)

* Prefills email from `?email=` or `localStorage(cr_last_email | cr_user_email)`.
* On success with confirm‑by‑email: shows “Check your email…”.
* If `409 Conflict`: shows “Your account is already registered. Please sign in.” and surfaces a “Go to login” link prefilled with `?email=<user>`.

### Contribute page (`frontend/contribute.html`)

* Shows **only** the signed‑in user’s name + email using the logic above.

---

## Errors (canonical)

* `400/422` – invalid data
* `401` – not authenticated
* `409` – duplicate user (signup)

All error responses are:

```json
{ "error": "Human-readable message" }
```

---

## Environment variables (backend)

Place in `backend/.env`:

```
SUPABASE_URL=...
SUPABASE_SERVICE_ROLE_KEY=...
FLASK_ENV=development
```

If they’re missing, the backend raises a clear runtime error on startup.

---

## Quick tests

**Signup**

```bash
curl -s -X POST http://127.0.0.1:5000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"name":"Eman Alasaadi","email":"eman.alasaadi5@gmail.com","password":"secret"}'
```

**Login (save cookie)**

```bash
curl -i -c cookies.txt -X POST http://127.0.0.1:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"eman.alasaadi5@gmail.com","password":"secret"}'
```

**Me (with cookie)**

```bash
curl -b cookies.txt http://127.0.0.1:5000/api/auth/me
```

---

# docs/architecture.md — System & Flow

## High‑level view

```
[Frontend (HTML/JS/CSS)]  <--fetch JSON-->  [Flask API]  <--->  [Supabase (Auth + Postgres)]
         |                                          ^
         | (session cookie; localStorage)           |
         +-------------------- shows current user ---+
```

* **Frontend**: Vanilla HTML/CSS/JS; pages: `index.html`, `login.html`, `signup.html`, `contribute.html`.
* **Backend**: Flask app under `/api`; auth blueprint provides `/auth/signup`, `/auth/login`, `/auth/me`.
* **Database**: Supabase (Postgres) with Auth; the app associates the Supabase Auth user with a row in `public.users` via `users.auth_uid` and uses RLS for safety.

## Auth & session flow

1. **Signup** → backend creates auth user; may send email confirmation.
2. **Login** → backend verifies credentials and sets an HTTP‑only **session cookie**.
3. **/auth/me** → reads cookie, returns `{ user: { name, email } }`.
4. **Frontend caching**

   * `cr_user_name`, `cr_user_email` are stored after login for instant rendering.
   * `cr_last_email` stored at signup to prefill login later.

## “Current user only” rendering

* The **Contribute** page **never** queries a list of users.
* It calls `/auth/me`; if unavailable, it uses the cached `{name,email}` from localStorage.
* It renders exactly **one** card (`.faq-card`) with that user’s name and mailto link.

## Security notes

* Session cookie is HTTP‑only; frontend cannot read its value (only sends it automatically).
* Row‑Level Security (RLS) in Postgres (via Supabase) ensures:

  * A user can only read/update their own user row and bookings.
  * Public read is allowed only for safe resources (e.g., vehicles list), if you enable that.

## Frontend structure

```
frontend/
  index.html             # Home
  login.html             # Sign in (prefill, stores name/email, redirects)
  signup.html            # Create account (prefill; email confirm support)
  contribute.html        # Shows only the current logged‑in user
  assets/…               # images, css, etc.
```

Key JS behaviors (inline per page):

* **login.html**: prefill + POST `/auth/login` + cache name/email.
* **signup.html**: prefill + POST `/auth/signup`; handles 409 and confirm‑by‑email.
* **contribute.html**: `GET /auth/me` → render one card; fallback to localStorage.

## Backend structure

```
backend/
  app.py                 # Flask app factory + blueprints
  api/
    auth.py              # /api/auth/* endpoints (signup, login, me, (logout?))
  db/
    init_supabase.py     # client creation from .env (URL + service role key)
  requirements.txt
```

## Local dev

* Start backend

  ```
  cd backend
  python app.py
  ```
* Open frontend (Live Server or any static server), e.g.

  ```
  http://127.0.0.1:5500/frontend/login.html
  http://127.0.0.1:5500/frontend/contribute.html
  ```
* Ensure `API_BASE` used by pages is `http://127.0.0.1:5000/api`.

## Future extensions

* Add `/auth/logout` endpoint and a **Sign out** menu under the username in the navbar (clears cookie server‑side and `localStorage` client‑side).
* Add profile editing (`PATCH /auth/me`) governed by RLS (only self).
