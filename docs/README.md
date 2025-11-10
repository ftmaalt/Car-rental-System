# 🚗 Cruzr Car Rental System

Welcome to **Cruzr**, an open-source web application for browsing, booking, and paying for rental cars — built by students from the **University of Bahrain**.  
Our goal is to make car rentals simple, fast, and secure, while maintaining open and respectful collaboration for developers and users alike. 💙  

---

## ✨ Key Features
### 🖥️ User Interface
- Clean, modern design using **Cruzr’s blue–teal color palette**.  
- Responsive layout for desktop and mobile.  
- Intuitive **Help Page** with searchable FAQ and contact form.

### 💳 Payment System
- Integrated **Stripe Checkout Flow** (test mode).  
- Secure success/cancel pages for transaction feedback.  
- **Stripe Webhook Handler** for verifying payments automatically on the backend.

### 💬 Help & Support
- Searchable **FAQ Accordion** powered by a `faq.json` file for easy editing.  
- **Blue Support Button** at the bottom-right corner opens a contact form.  
- Messages sent via **EmailJS** directly to our support inbox — no mailto links needed.

### 📜 Open-Source Documentation
- `CODE_OF_CONDUCT.md` → Ensures a friendly and safe community.  
- `CONTRIBUTING.md` → Guides new developers through contributing process.  
- Both documents available publicly on GitHub.

---

## ⚙️ Tech Stack
| Layer | Technologies Used |
|-------|--------------------|
| **Frontend** | HTML, CSS, JavaScript (with TailwindCSS styling),python |
| **Backend** | Node.js, Stripe API (test mode) |
| **Data** | JSON for FAQs and configuration |
| **Email Integration** | EmailJS |
| **Hosting** | GitHub Pages / Netlify *(depending on deployment)* |

---

## 🧩 Project Structure
CAR-RENTAL-SYSTEM/
├─ .vscode/
├─ assets/
│  ├─ customer-support.png
│  ├─ darkmode.svg
│  ├─ dev-guide.svg
│  ├─ docs.svg
│  ├─ googlemaps.svg
│  ├─ lightmode.svg
│  ├─ logo.png
│  ├─ manage-booking.svg
│  └─ search.svg
├─ backend/
├─ docs/
│  ├─ api.md
│  └─ architecture.md
├─ CODE_OF_CONDUCT.md
├─ CONTERBUTING.md   ← rename to CONTRIBUTING.md
├─ Features.md
├─ frontend/
│  ├─ booking.css
│  ├─ booking.html
│  ├─ booking.js
│  ├─ contribute.css
│  ├─ contribute.html
│  ├─ darkmode.js
│  ├─ downloads.html
│  ├─ faq.json
│  ├─ help.css
│  ├─ help.html
│  ├─ homepage.css
│  ├─ login.html
│  ├─ signup.html
│  └─ index.html
└─ LICENSE

---

🤝 Contributing

We’d love your help!
Please read our Contributing Guide
 for setup instructions, coding standards, and how to open pull requests.

Make sure to also check our Code of Conduct
 — kindness and respect make collaboration better for everyone. 💬

---
🏫 Course

ITSE476 — Free and Open-Source Software Development, University of Bahrain      

---

## 🚀 Run Locally

    1. Fork the Repository
Go to our GitHub repo and click **Fork** to create your own copy.

    2. Clone Your Fork
git clone https://github.com/<your-username>/Cruzr-Car-Rental-System.git
cd Cruzr-Car-Rental-System

    3. Create a new branch
Give your branch a clear name describing what you’re working on: 
    git checkout -b feature/help-page-update
or
    git checkout -b fix/faq-search-bug

    4. Make Your Changes
-If you’re working on the frontend, keep the style consistent with our blue–teal color palette.
-If you’re editing the Help Page, store FAQ questions inside the JSON file (not directly in HTML).
-If you’re touching backend logic, test everything in Stripe’s test mode first.
-For docs, keep things clear and easy for new contributors to understand.

    5. Test Before You Push
-Open your page in the browser and make sure nothing breaks.
-Check buttons, forms, and the blue support circle to ensure it works smoothly.
-Make sure your console shows no major errors.

    6. Commit Your Changes
-Write a short, clear commit message: 
    git commit -m "Add contact form email integration"

    7. Push and Open a Pull Request
git push origin feature/help-page-update
    -Then go back to your fork on GitHub and click “New Pull Request”.
    -Describe what you changed and why — screenshots are always appreciated!


---


👩‍💻 Team Members & Contributions

Fatima Mohamed Hasan Abdulla    202206839
Frontend: Home page (project info + announcements)
Backend: Vehicle search endpoint
Hosting: Deployed frontend on Vercel
Docs: Features & Requirements
✅ Deliverables: Homepage + working search + deployment + features list

Eman Yaser Alasaadi              202205182
Frontend: Contributors page (resources, downloads, issues)
Backend: Booking API (create & cancel booking)
Hosting: Supabase DB schema & seed data
Docs: Architecture & API documentation
✅ Deliverables: Contributors page + booking API + DB setup + API docs

Yusra Husain Haji                202009756
Frontend: Booking page (car rental interface)
Backend: Stripe checkout flow (test mode + success/cancel)
DevOps: CI/CD on GitHub (lint + test workflow)
Docs: Contributing Guide + Code of Conduct
✅ Deliverables: Booking page + payments + CI workflow + guidelines

Laila Mahmood Mohammed Haji       202204640
Frontend: Help page (FAQ accordion + blue support contact form)
Docs: README, FAQ, Code of Conduct, Contributing Guide, and Announcements
✅ Deliverables: Help page + full project documentation + announcements system

---

🧠 Lessons Learned

Managing collaboration with GitHub branching & issues.
Building consistent UI with Cruzr’s blue–teal theme.
Applying open-source documentation standards.
Deploying and testing with Vercel and Supabase.

---
📄 License

This project is licensed under the MIT License.
Feel free to fork, modify, and use it for learning or open-source purposes.

---

A Note from the Team

“Cruzr was built with passion, patience, and teamwork.
Our goal was to create a functional, open-source car rental platform that’s easy to use and easy to improve.
Every page, feature, and document was made collaboratively — and we’re proud to share it with the community.” 🚘✨
