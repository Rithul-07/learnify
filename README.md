# 📚 Learnify — Online Learning Platform

A full-stack web application built with **HTML/CSS/JavaScript**, **Flask**, and **MySQL**.
Students enroll in courses, track progress, and earn certificates.
Instructors create and manage content. Admins oversee everything.

---

## 🗂️ Project Structure

```
learnify/
├── app.py                  # Flask app factory & entry point
├── config.py               # DB and secret config
├── requirements.txt        # Python dependencies
├── schema.sql              # Full MySQL schema + seed data
│
├── routes/
│   ├── __init__.py
│   ├── auth.py             # Register, login, logout, profile
│   ├── courses.py          # Browse, detail, enroll, review
│   ├── student.py          # Dashboard, learning, progress, certificates
│   ├── instructor.py       # Create/edit courses, sections, lessons, quizzes
│   └── admin.py            # Users, courses, analytics, settings
│
├── static/
│   ├── css/
│   │   └── style.css       # Global styles (variables, layout, components)
│   └── js/
│       └── main.js         # UI interactions, AJAX calls, progress tracking
│
└── templates/
    ├── base.html            # Navbar, flash messages, footer
    ├── index.html           # Landing page with featured courses
    ├── register.html        # Sign up (student / instructor)
    ├── login.html           # Login page
    ├── profile.html         # Edit profile & bio
    ├── courses.html         # Browse & filter all courses
    ├── course_detail.html   # Course page with syllabus & reviews
    ├── learn.html           # Lesson player with video + notes
    ├── dashboard.html       # Student: enrolled courses + progress
    ├── certificates.html    # Student: earned certificates
    │
    ├── instructor/
    │   ├── dashboard.html   # Instructor: stats + course list
    │   ├── course_form.html # Create / edit course
    │   ├── curriculum.html  # Manage sections + lessons
    │   └── quiz_form.html   # Create quiz with questions
    │
    └── admin/
        ├── dashboard.html   # Platform stats overview
        ├── users.html       # Manage all users
        ├── courses.html     # Approve / archive courses
        └── analytics.html  # Enrollment & revenue charts
```

---

## 🛠️ Tech Stack

| Layer      | Technology                        |
|------------|-----------------------------------|
| Frontend   | HTML5, CSS3, Vanilla JavaScript   |
| Backend    | Python 3.10+, Flask 3.0           |
| Database   | MySQL 8.0                         |
| Auth       | Flask sessions + Werkzeug hashing |
| Styling    | Custom CSS with CSS variables     |

---



## 👥 User Roles

| Role       | Capabilities                                                      |
|------------|-------------------------------------------------------------------|
| Student    | Browse & enroll in courses, watch lessons, take quizzes, get certs|
| Instructor | Create courses, add sections/lessons/quizzes, view student stats  |
| Admin      | Manage all users, approve/archive courses, view platform analytics|


---

## 🗄️ Database Tables

| Table             | Purpose                              |
|-------------------|--------------------------------------|
| users             | All users with roles                 |
| categories        | Course categories (8 seeded)         |
| courses           | Course metadata, status, price       |
| sections          | Ordered sections within a course     |
| lessons           | Video lessons inside sections        |
| enrollments       | Student ↔ Course relationships       |
| lesson_progress   | Per-lesson completion tracking       |
| quizzes           | Quiz linked to a course/lesson       |
| quiz_questions    | MCQ questions with 4 options         |
| quiz_attempts     | Student scores per quiz              |
| reviews           | Star ratings + comments per course   |
| certificates      | Auto-issued on course completion     |

---

## ✨ Features

### Student
- Register/login, edit profile and bio
- Browse courses by category, level, search, sort
- Enroll in free courses with one click
- Watch lessons with embedded video player
- Track lesson completion progress (% per course)
- Take MCQ quizzes and see pass/fail results
- Leave star ratings and written reviews
- Download certificates on course completion

### Instructor
- Register as instructor at signup
- Create courses with title, description, category, level, price
- Add sections and lessons (title, video URL, duration, preview flag)
- Mark lessons as free preview (visible without enrollment)
- Create quizzes with MCQ questions and pass threshold
- View enrolled student count and average rating per course

### Admin Panel
- Full stats dashboard (users, courses, enrollments, revenue)
- View, activate/deactivate, or delete any user
- Approve instructor-created courses before they go live
- Archive or delete courses
- View enrollment and rating analytics

---

## 🔑 Key Flask Concepts Practiced

- **Blueprints** — modular route organization by role
- **Flask Sessions** — user authentication state
- **MySQL raw queries** — joins, aggregates, subqueries
- **Role-based access control** — decorator-based guards
- **Flash messages** — user feedback system
- **Jinja2 templating** — template inheritance with `base.html`
- **AJAX / Fetch API** — dynamic progress updates without page reload
- **Password hashing** — Werkzeug `generate_password_hash`

---

## 📋 API-style Routes Summary

### Auth
| Method | Route          | Description          |
|--------|----------------|----------------------|
| GET    | /              | Home / landing page  |
| GET    | /register      | Register form        |
| POST   | /register      | Create account       |
| GET    | /login         | Login form           |
| POST   | /login         | Authenticate user    |
| GET    | /logout        | Clear session        |
| GET/POST | /profile     | View/edit profile    |

### Courses
| Method | Route                        | Description           |
|--------|------------------------------|-----------------------|
| GET    | /courses                     | Browse all courses    |
| GET    | /course/<slug>               | Course detail page    |
| POST   | /course/<id>/enroll          | Enroll in course      |
| POST   | /course/<id>/review          | Submit review         |

### Student
| Method | Route                        | Description           |
|--------|------------------------------|-----------------------|
| GET    | /dashboard                   | Student dashboard     |
| GET    | /learn/<course_id>           | Lesson player         |
| POST   | /lesson/<id>/complete        | Mark lesson done      |
| GET    | /certificates                | View certificates     |
| GET    | /quiz/<id>                   | Take quiz             |
| POST   | /quiz/<id>/submit            | Submit quiz           |

### Instructor
| Method | Route                        | Description           |
|--------|------------------------------|-----------------------|
| GET    | /instructor/                 | Instructor dashboard  |
| GET/POST | /instructor/course/new     | Create course         |
| GET/POST | /instructor/course/<id>    | Edit course           |
| GET    | /instructor/course/<id>/curriculum | Manage curriculum |
| POST   | /instructor/section/add      | Add section           |
| POST   | /instructor/lesson/add       | Add lesson            |
| GET/POST | /instructor/quiz/<course_id> | Create quiz         |

### Admin
| Method | Route                        | Description           |
|--------|------------------------------|-----------------------|
| GET    | /admin/                      | Admin dashboard       |
| GET    | /admin/users                 | Manage users          |
| GET    | /admin/users/<id>/<action>   | Activate/delete user  |
| GET    | /admin/courses               | Manage courses        |
| GET    | /admin/courses/<id>/<action> | Approve/archive       |
| GET    | /admin/analytics             | Platform analytics    |

---

## 🚀 Production Checklist

- [ ] Change `SECRET_KEY` to a long random string
- [ ] Set `DEBUG = False` in config
- [ ] Use environment variables for DB credentials (`.env` + `python-dotenv`)
- [ ] Add file upload support for thumbnails (Flask + `werkzeug.utils.secure_filename`)
- [ ] Integrate a real payment gateway (Razorpay/Stripe) for paid courses
- [ ] Add email notifications (Flask-Mail) for enrollment and certificates
- [ ] Deploy on a VPS (Ubuntu + Gunicorn + Nginx)
- [ ] Use HTTPS with Let's Encrypt SSL certificate

---


