✅ `docs/architecture.md`
```markdown
#  Cruzr Car Rental – System Architecture
**Author:** Eman Yaser Alasaadi 
**Role:** Backend – Booking API, Users Page, Database Schema & Docs

---

## 1. Overview
The **Cruzr Car Rental System** is a full-stack web application built with:
- **Frontend:** HTML, CSS, and JavaScript  
- **Backend:** Python Flask (API layer)  
- **Database & Auth:** Supabase (PostgreSQL + Authentication + RLS)

It enables users to sign up, log in, and make car bookings securely.

---

## 2. System Components
┌────────────────────────────┐
│ Frontend (HTML/CSS/JS) │
│ ─ Pages: index, login, │
│ signup, contribute │
└───────────┬────────────────┘
│ JSON + Cookies
┌───────────▼────────────────┐
│ Flask Backend (app.py) │
│ /api/auth/* │
│ /api/bookings/* │
└───────────┬────────────────┘
│ Supabase SDK
┌───────────▼────────────────────────┐
│ Supabase (PostgreSQL + Auth) │
│ Tables: users, vehicles, bookings │
│ RLS: each user sees only theirs │
└────────────────────────────────────┘

---

## 3. Authentication Flow
1. **Signup:** user submits name, email, password → backend calls Supabase Auth → Supabase stores user.  
2. **Login:** Supabase verifies credentials → returns session tokens → Flask sets cookies.  
3. **/auth/me:** verifies cookies → returns `{ user: { name, email } }`.  
4. **Logout:** clears cookies.

Frontend uses `fetch(..., { credentials:"include" })` to send/receive cookies.

---

## 4. Booking Workflow
1. User logs in (session established).  
2. Frontend sends `POST /bookings` with car + date range.  
3. Backend inserts into `bookings` table on Supabase.  
4. User can later cancel with `DELETE /bookings/<id>`.  
5. All operations respect RLS: a user can only view or modify their own bookings.

---

## 5. Data Schema
| Table | Description | Key Columns |
|--------|--------------|-------------|
| **users** | Registered app users | `id`, `name`, `email`, `auth_uid` |
| **vehicles** | Cars available for rent | `id`, `make`, `model`, `status` |
| **bookings** | Reservations by users | `id`, `user_id`, `vehicle_id`, `start_at`, `end_at`, `total_amount` |
| **payments** | Payment records | `id`, `booking_id`, `status`, `amount` |

---

## 6. Security
- Supabase Row-Level Security (RLS) policies enforce user isolation.  
- Backend uses the **Service Role Key** for administrative actions.  
- Frontend never exposes secret keys.  
- Auth cookies are `HttpOnly`, `SameSite=Lax`.

---

## 7. Unique Feature: Personalized Contributor Page
- `contribute.html` calls `/auth/me` to display **only the logged-in user’s** name and email.  
- This replaces generic contributor lists and personalizes the view for each authenticated user.

---

## 8. Deployment & Hosting
- **Backend:** Flask (localhost during dev, deployable to Render or Heroku)  
- **Frontend:** Static hosting (Vercel / GitHub Pages)  
- **Database:** Supabase cloud instance (PostgreSQL)  

Frontend and backend communicate via REST over `http://127.0.0.1:5000/api`.

---

## 9. Future Enhancements
- Add booking history & admin dashboard  
- Integrate Stripe for real payments  
- Improve UI responsiveness  
- Deploy public demo URL

---

## 10. Summary
This architecture provides:
- A secure authentication mechanism  
- A clear separation of frontend and backend  
- Simple RESTful API endpoints  
- Supabase integration with strong data security  

Eman Yaser Alasaadi  
*Backend Developer & Technical Documentation Lead*

---

*End of `architecture.md`*
