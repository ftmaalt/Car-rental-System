# 🚗 Cruzr — Features & Requirements

### Version 1.0 (Phase-1)
_Last updated: November 2025_

---

## 🌟 Overview
**Cruzr** is an open-source car rental and ride-finding website that helps users **search, filter, and simulate bookings** for vehicles in various locations.  
It is designed to be beginner-friendly, lightweight, and open for public contributions.

---

## ✨ Current Features

### 🧭 For Users
- **Homepage**
  - Project overview and navigation.
  - Light/Dark mode theme switcher.
  - “How it Works” and “Features” sections.

- **Booking Page**
  - Search by pickup location and dates.
  - Filters for:
    - Vehicle Type (SUV, Sedan, Electric, Luxury)
    - Price Range (slider)
    - Rating and Availability  
  - Dynamic vehicle cards with image or placeholder icon.
  - “Book Now” demo button (no payment yet).

- **Help Center**
  - Searchable FAQs with highlight results.
  - Category chips for quick filtering.
  - Floating Support Button (FAB) → mini contact form (Formspree or mail).

- **Announcements**
  - Project news such as feature releases and development updates.

- **Downloads / Docs**
  - PDF and Markdown documents: API, Architecture, Guidelines, and Code of Conduct.

---

### 🧑‍💻 For Contributors
- Public GitHub repository (open for forks and pull requests).
- Developer Guidelines and Code of Conduct.
- Contribution workflow with issues, commits, and discussions.
- GitHub Discussions and Discord server for communication.
- Documentation pages for:
  - Architecture overview  
  - API endpoints  
  - Resources and issues  

---

## ⚙️ Requirements

### 🌐 User Requirements
- Modern web browser (Chrome, Edge, Firefox, or Safari).
- Internet connection for live website access.
- JavaScript enabled (for search and filters).
- Active email to contact support or use the Formspree form.

### 💻 Developer Requirements
- GitHub account for collaboration.
- Code editor (VS Code recommended).
- Git installed for version control.
- Python 3.x with Flask and Flask-CORS for the backend API.
- Optional: Node.js or Live Server for local testing.

**Local setup:**
```bash
git clone https://github.com/username/cruzr.git
cd cruzr/backend
pip install flask flask-cors
python booking_api.py
python app.py
