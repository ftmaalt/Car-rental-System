# docs/architecture.md — System & Flow

## High-level view

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
2. **Login** → backend verifies credentials and sets an HTTP-only **session cookie**.
3. **/auth/me** → reads cookie, returns `{ user: { name, email } }`.
4. **Frontend caching**

   * `cr_user_name`, `cr_user_email` are stored after login for instant rendering.
   * `cr_last_email` stored at signup to prefill login later.

## “Current user only” rendering

* The **Contribute** page **never** queries a list of users.
* It calls `/auth/me`; if unavailable, it uses the cached `{name,email}` from localStorage.
* It renders exactly **one** card (`.faq-card`) with that user’s name and mailto link.

## Security notes

* Session cookie is HTTP-only; frontend cannot read its value (only sends it automatically).
* Row-Level Security (RLS) in Postgres (via Supabase) ensures:

  * A user can only read/update their own user row and bookings.
  * Public read is allowed only for safe resources (e.g., vehicles list), if you enable that.

## Frontend structure

```
frontend/
  index.html             # Home
  login.html             # Sign in (prefill, stores name/email, redirects)
  signup.html            # Create account (prefill; email confirm support)
  contribute.html        # Shows only the current logged-in user
  assets/…               # images, css, etc.
```

Key JS behaviors (inline per page):

* **login.html**: prefill + POST `/auth/login` + cache name/email.
* **signup.html**: prefill + POST `/auth/signup`; handles 409 and confirm-by-email.
* **contribute.html**: `GET /auth/me` → render one card; fallback to localStorage.

## Backend structure

```
backend/
  app.py                 # Flask app factory + blueprints
  api/
    auth.py              # /api/auth/* endpoints (signup, login, me, logout)
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

## 📌 Equal Workload Division (Each member: Frontend + Backend + Hosting/DevOps + Docs)

**Fatima Mohamed Hasan Abdulla**

* **Frontend:** Build Main page (home with project info, announcements).
* **Backend:** Implement Vehicle search endpoint (basic query with filters).
* **Hosting/DevOps:** Deploy frontend app on Vercel (connect repo).
* **Docs:** Write Features & Requirements section.
  ✅ *Delivers:* Homepage + working search + deployment + features list.

---

**Eman Yaser Alasaadi**

* **Frontend:** Build Contributors page (resources, downloads, issues link).
* **Backend:** Implement Booking API (create & cancel booking).
* **Hosting/DevOps:** Set up Supabase DB schema & seed data.
* **Docs:** Write Architecture & API docs (`docs/architecture.md`, `docs/api.md`).
  ✅ *Delivers:* Contributors page + bookings backend + DB + API docs.

---

**Yusra Husain Haji**

* **Frontend:** Build booking page 
* **Backend:** Implement Stripe checkout flow (test mode, success/cancel pages).
* **Hosting/DevOps:** Configure CI/CD on GitHub (lint + test workflow).
* **Docs:** Write Contributing Guide + Code of Conduct.
  ✅ *Delivers:* Users page + payments + CI + guidelines.

---

**Laila Mahmood Mohammed Haji**

* **Frontend:** Build Help page (FAQ accordion + contact form).
* **Backend:** Implement Stripe webhook handler (update booking status).
* **Hosting/DevOps:** Publish Release v0.1.0 on GitHub (downloads + screenshots).
* **Docs:** Write README, FAQ, and manage Announcements (site + GitHub Discussions).
  ✅ *Delivers:* Help page + webhook + release + full project docs.

---

## 10. Summary

This architecture provides:

* A secure authentication mechanism
* A clear separation of frontend and backend
* Simple RESTful API endpoints
* Supabase integration with strong data security

### 📘 Additional Summary — CRS Project Requirement Overview

The **Cruzr Car Rental System (CRS)** is built following the *Software Requirements Specification* principles defined for the project in collaboration with the University of Bahrain, College of IT.

**Purpose:**
The CRS aims to connect users, drivers, and rental providers under one platform for renting vehicles or hiring drivers easily and securely.

**Scope:**
Users can register, log in, search for vehicles or drivers, make bookings, process payments, and manage reservations. The system supports insurance, GPS tracking, fare calculation, and refund policies.

**Functional Highlights:**

* **User Management:** Registration, login/logout, and profile management.
* **Service Selection:** Choose between renting a vehicle or hiring a driver.
* **Search & Booking:** Filter listings by price, location, or rating.
* **Fare Calculation & Payment:** Real-time calculation with multiple payment methods.
* **Insurance Integration:** Drivers and users can manage or renew policies.
* **Customer Support Tools:** Live chat, complaint handling, and driver assistance.

**Non-Functional Requirements:**

* **Performance:** Supports >1000 concurrent users.
* **Reliability:** 99.9% uptime target.
* **Security:** AES-256 encryption and role-based authentication.
* **Scalability:** Up to 6000 bookings per day.
* **Maintainability:** Code maintainability index ≥ 80%.

**Stakeholders:**
Customers, drivers, rental companies, developers, payment gateways, insurers, and regulatory authorities.

**System Components (Team Roles)**
See *Equal Workload Division* above for detailed task allocation.

**Use Cases (Example Highlights):**

* **Book a Driver or Car:** Search → Select → Confirm → Pay.
* **Modify or Cancel Booking:** Users can change or cancel before deadline.
* **Payment & Refunds:** Real-time transaction and 24-hour refund processing.
* **Insurance Management:** Drivers renew or select policies in-app.
* **Customer Support:** Live chat, complaint resolution, and troubleshooting.

**Design Alignment:**
These requirements directly influence the system’s architecture and explain how each subsystem (booking, payment, support, and insurance) integrates under the same authentication and data framework powered by Flask + Supabase.

---

Eman Yaser Alasaadi
*Backend Developer & Technical Documentation Lead*

---

*End of `architecture.md`*
