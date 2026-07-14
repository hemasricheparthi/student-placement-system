# Student Placement Management System

A professional, industry-level **Student Placement Management System** built with **Python, Django, Bootstrap 5, and SQLite**. Designed for final-year engineering projects and software company interviews (Infosys, TCS, Cognizant, Capgemini, Accenture, Wipro, Deloitte, etc.).

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Django](https://img.shields.io/badge/Django-5.0+-green)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Features

### User Roles
- **Admin** — Manage users, departments, drives, announcements, analytics
- **Placement Officer** — Verify profiles, manage drives, generate reports, CSV export
- **Student** — Profile, resume upload, apply for jobs, track applications, interviews, offers
- **Company/Recruiter** — Post jobs, view applicants, shortlist, schedule interviews, issue offers

### Smart Resume Match System
- Extracts text from PDF resumes using **PyPDF2**
- Matches resume skills against job requirements
- Displays **Match Percentage**, **Missing Skills**, and **Suggested Skills**
- No external AI APIs — pure Python implementation

### Dashboard & Analytics
- Real-time statistics with **Chart.js** graphs
- Placement percentage, department-wise breakdown
- Monthly application trends

### Additional Features
- Notifications system
- Search & filters (CGPA, department, skills, status)
- Pagination, form validation, flash messages
- Password reset, profile management
- CSV report export
- Mobile responsive Bootstrap 5 UI

---

## Project Structure

```
student-placement-system/
├── placement_portal/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/                  # Authentication, roles, departments, skills
├── students/                  # Student profiles, certifications, projects, resumes
├── companies/                 # Company profiles and verification
├── jobs/                      # Job postings, applications, resume matcher
├── placement/                 # Drives, interviews, offer letters
├── dashboard/                 # Role-based dashboards with Chart.js
├── reports/                   # Reports and CSV export
├── templates/                 # HTML templates (Bootstrap 5)
├── static/                    # CSS, JavaScript
├── media/                     # Uploaded files (resumes, logos)
├── requirements.txt
├── manage.py
└── README.md
```

---

## Installation Guide

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/student-placement-system.git
cd student-placement-system
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Load Sample Data
```bash
python manage.py load_sample_data
```

### Step 6: Run Development Server
```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000/** in your browser.

---

## Default Login Credentials

| Role              | Username  | Password    |
|-------------------|-----------|-------------|
| Admin             | admin     | admin123    |
| Placement Officer | officer   | officer123  |
| Student           | student1  | student123  |
| Company (TCS)     | tcs       | company123  |

---

## Django Commands Reference

```bash
# Create superuser manually
python manage.py createsuperuser

# Load sample data
python manage.py load_sample_data

# Collect static files (production)
python manage.py collectstatic

# Run tests
python manage.py test

# Django shell
python manage.py shell
```

---

## Database Models

| Model            | App        | Description                          |
|------------------|------------|--------------------------------------|
| CustomUser       | accounts   | User with role-based access          |
| Department       | accounts   | Academic departments                 |
| Skill            | accounts   | Skills database for matching         |
| Notification     | accounts   | In-app notifications                 |
| StudentProfile   | students   | Student academic & placement info    |
| Resume           | students   | PDF resume with extracted skills     |
| CompanyProfile   | companies  | Company/recruiter profiles           |
| Job              | jobs       | Job openings with eligibility        |
| Application      | jobs       | Applications with match percentage   |
| PlacementDrive   | placement  | Campus placement events              |
| Interview        | placement  | Interview scheduling               |
| OfferLetter      | placement  | Offer management                   |

---

## Smart Resume Match — How It Works

1. Student uploads PDF resume
2. System extracts text using **PyPDF2**
3. Skills are identified via pattern matching against a skill database
4. On job application, resume skills are compared with job requirements
5. Results displayed:
   - **Match Percentage** = (matched skills / required skills) × 100
   - **Missing Skills** = required skills not found in resume
   - **Suggested Skills** = complementary skills to learn

---

## API Endpoints (URL Routes)

| URL Pattern                    | Description                |
|--------------------------------|----------------------------|
| `/`                            | Home page                  |
| `/accounts/login/`             | Login                      |
| `/accounts/register/student/`  | Student registration       |
| `/accounts/register/company/`  | Company registration       |
| `/dashboard/admin/`            | Admin dashboard            |
| `/dashboard/officer/`          | Officer dashboard          |
| `/dashboard/student/`          | Student dashboard          |
| `/dashboard/company/`          | Company dashboard          |
| `/jobs/`                       | Job listings               |
| `/jobs/eligible/`              | Eligible jobs (student)    |
| `/companies/`                  | Company list               |
| `/reports/`                    | Reports & CSV export       |
| `/admin/`                      | Django admin panel         |

---

## Screenshots & UI Design

The application uses a modern **Bootstrap 5** interface with:
- **Primary blue** navbar with role-based navigation
- **Stat cards** on dashboards with icons
- **Chart.js** bar/line/doughnut charts for analytics
- **Match score bars** with color coding (green > 70%, yellow > 40%, red < 40%)
- **Skill tags** for matched/missing/suggested skills
- **Responsive tables** with pagination
- **Flash messages** for user feedback

---

## Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test accounts
python manage.py test jobs
```

---

## Production Deployment Notes

1. Change `SECRET_KEY` in `settings.py`
2. Set `DEBUG = False`
3. Configure `ALLOWED_HOSTS`
4. Use PostgreSQL instead of SQLite for production
5. Set up proper email backend for password reset
6. Run `python manage.py collectstatic`
7. Use Gunicorn/uWSGI with Nginx

---

## Technologies Used

- **Backend:** Python 3, Django 5+
- **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript
- **Charts:** Chart.js
- **Database:** SQLite (dev) / PostgreSQL (prod)
- **PDF Processing:** PyPDF2
- **Forms:** django-crispy-forms + crispy-bootstrap5

---

## Author

Built as a final-year engineering project demonstrating full-stack Django development with role-based access control, smart matching algorithms, and production-quality code architecture.

---

## License

MIT License — Free to use for educational and portfolio purposes.
