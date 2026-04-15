from flask import Blueprint, render_template, current_app
from mock_data import COURSES, CATEGORIES

views_bp = Blueprint('views', __name__)


@views_bp.route('/')
def home():
    # ── Featured courses (latest 3 published) ────────────────
    if current_app.config.get('MYSQL_AVAILABLE'):
        try:
            cur = current_app.mysql.connection.cursor()
            cur.execute('''
                SELECT c.*, cat.name AS category_name, cat.icon AS category_icon,
                       (SELECT COUNT(*) FROM enrollments e WHERE e.course_id = c.id) AS enrolled_count,
                       (SELECT COUNT(*) FROM lessons l WHERE l.course_id = c.id) AS total_lessons
                FROM courses c
                LEFT JOIN categories cat ON c.category_id = cat.id
                WHERE c.status = 'published'
                ORDER BY c.created_at DESC LIMIT 6
            ''')
            featured = cur.fetchall()
            cur.execute('SELECT COUNT(*) AS cnt FROM users WHERE role="student"')
            total_students = cur.fetchone()['cnt']
            cur.execute('SELECT COUNT(*) AS cnt FROM courses WHERE status="published"')
            total_courses = cur.fetchone()['cnt']
            cur.execute('SELECT COUNT(*) AS cnt FROM enrollments')
            total_enrollments = cur.fetchone()['cnt']
            cur.close()
        except Exception:
            featured = COURSES[:6]
            total_students = 2847
            total_courses = len(COURSES)
            total_enrollments = 1580
    else:
        featured = COURSES[:6]
        total_students = 2847
        total_courses = len(COURSES)
        total_enrollments = 1580

    stats = {
        'students': total_students,
        'courses': total_courses,
        'enrollments': total_enrollments,
    }
    return render_template('home.html', featured=featured, stats=stats,
                           categories=CATEGORIES)
