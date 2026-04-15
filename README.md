# 🎓 Learnify

A complete, full-stack online learning platform inspired by **The Odin Project** and **freeCodeCamp**. Built with Flask, MySQL, Jinja2, and a stunning glassmorphism UI — zero Bootstrap.

---

## ✨ Features

### Student
- Register / Login with session-based auth
- Browse & search courses with filters (category, level, sort)
- View course syllabus with accordion sections
- Enroll in courses (free)
- Track progress lesson-by-lesson
- Earn certificates on course completion

### Admin
- Register with secret admin key
- Dashboard with platform stats & recent enrollments
- Create courses with dynamic sections & lessons
- Manage students: activate, deactivate, delete
- Delete courses

---

## 🛠️ Tech Stack

| Layer      | Technology                          |
|------------|-------------------------------------|
| Frontend   | HTML5, Vanilla CSS, JavaScript      |
| Backend    | Python Flask (Blueprints)           |
| Database   | MySQL (Flask-MySQLdb, DictCursor)   |
| Templating | Jinja2                              |
| Auth       | Werkzeug password hashing + sessions|
| Design     | Custom glassmorphism (no Bootstrap) |
| Font       | Poppins (Google Fonts)              |

---

## 📁 Project Structure

```
learnify/
├── routes/
│   ├── __init__.py      # login_required & admin_required decorators
│   ├── auth.py           # register, login, logout
│   ├── views.py          # home page
│   ├── courses.py        # course list, detail, enroll, complete lesson
│   ├── student.py        # student dashboard, progress tracker
│   └── admin.py          # admin dashboard, post course, manage students
├── static/
│   ├── css/style.css     # 900+ line glassmorphism design system
│   └── js/main.js        # hamburger menu, accordion, dynamic forms, counters
├── templates/
│   ├── admin/
│   │   ├── dashboard.html
│   │   ├── post_course.html
│   │   └── manage_students.html
│   ├── student/
│   │   ├── dashboard.html
│   │   └── progress.html
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── courses.html
│   └── course_detail.html
├── app.py               # Flask app factory
├── config.py            # Configuration (MySQL, secrets)
├── mock_data.py         # Sample data for demo mode (no DB needed)
├── schema.sql           # Complete MySQL schema (8 tables)
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### 1. Clone & Setup
```bash
cd learnify
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
```

### 2. Run (Demo Mode — No MySQL Required)
```bash
flask run --debug
```
Open http://127.0.0.1:5000

### 3. Demo Credentials
| Role    | Email               | Password  |
|---------|---------------------|-----------|
| Admin   | admin@learnify.com  | admin123  |
| Student | any email           | any pass  |

---

## 🗄️ Connect MySQL (Optional)

### 1. Create Database
```sql
mysql -u root -p < schema.sql
```

### 2. Update `config.py`
```python
MYSQL_HOST     = 'localhost'
MYSQL_USER     = 'root'
MYSQL_PASSWORD = 'your_password'
MYSQL_DB       = 'learnify'
```

### 3. Admin Registration
Register a new admin account by providing the secret key during registration.
Default secret: `learnify-admin-secret` (change in `config.py`)

---

## 🎨 Design System

- **Gradient Background:** `#0f0c29 → #302b63 → #24243e`
- **Glass Cards:** `backdrop-filter: blur(16px)`, semi-transparent borders
- **Accent Purple:** `#7c3aed` (hover: `#6d28d9`)
- **Font:** Poppins (300–800 weights)
- **Animations:** Fade-in, stagger, counter, accordion
- **Responsive:** Mobile hamburger menu, fluid grids

---

## 📄 License

MIT License. Built with 💜 for learners everywhere.
