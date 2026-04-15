from flask import Blueprint, render_template, session, current_app, redirect, url_for, flash
from routes import login_required
from mock_data import COURSES, ENROLLED_IDS, MOCK_PROGRESS, MOCK_CERTIFICATES, get_course_sections

student_bp = Blueprint('student', __name__)


@student_bp.route('/dashboard')
@login_required
def dashboard():
    enrolled_courses = []
    certificates = []

    if current_app.config.get('MYSQL_AVAILABLE'):
        try:
            cur = current_app.mysql.connection.cursor()
            cur.execute('''
                SELECT c.*, cat.name AS category_name, cat.icon AS category_icon,
                       e.enrolled_at, e.completed_at,
                       (SELECT COUNT(*) FROM lessons l WHERE l.course_id = c.id) AS total_lessons,
                       (SELECT COUNT(*) FROM lesson_progress lp
                        WHERE lp.user_id=%s AND lp.course_id=c.id AND lp.completed=1) AS completed_lessons
                FROM enrollments e
                JOIN courses c ON e.course_id = c.id
                LEFT JOIN categories cat ON c.category_id = cat.id
                WHERE e.user_id = %s
                ORDER BY e.enrolled_at DESC
            ''', (session['user_id'], session['user_id']))
            enrolled_courses = cur.fetchall()

            cur.execute('''
                SELECT cert.*, c.title AS course_title
                FROM certificates cert
                JOIN courses c ON cert.course_id = c.id
                WHERE cert.user_id = %s
                ORDER BY cert.issued_at DESC
            ''', (session['user_id'],))
            certificates = cur.fetchall()
            cur.close()
        except Exception:
            enrolled_courses = _mock_enrolled()
            certificates = MOCK_CERTIFICATES
    else:
        enrolled_courses = _mock_enrolled()
        certificates = MOCK_CERTIFICATES

    return render_template('student/dashboard.html',
                           enrolled_courses=enrolled_courses,
                           certificates=certificates)


@student_bp.route('/progress/<slug>')
@login_required
def progress(slug):
    course = None
    sections = []
    completed_lessons = []

    if current_app.config.get('MYSQL_AVAILABLE'):
        try:
            cur = current_app.mysql.connection.cursor()
            cur.execute('SELECT c.*, cat.name AS category_name FROM courses c LEFT JOIN categories cat ON c.category_id=cat.id WHERE c.slug=%s', (slug,))
            course = cur.fetchone()
            if course:
                cur.execute('SELECT * FROM sections WHERE course_id=%s ORDER BY position', (course['id'],))
                secs = cur.fetchall()
                for s in secs:
                    cur.execute('SELECT * FROM lessons WHERE section_id=%s ORDER BY position', (s['id'],))
                    s['lessons'] = cur.fetchall()
                sections = secs
                cur.execute('''
                    SELECT lesson_id FROM lesson_progress
                    WHERE user_id=%s AND course_id=%s AND completed=1
                ''', (session['user_id'], course['id']))
                completed_lessons = [r['lesson_id'] for r in cur.fetchall()]
            cur.close()
        except Exception:
            course = next((c for c in COURSES if c['slug'] == slug), None)
            if course:
                sections = get_course_sections(course['id'])
    else:
        course = next((c for c in COURSES if c['slug'] == slug), None)
        if course:
            sections = get_course_sections(course['id'])
            prog = MOCK_PROGRESS.get(course['id'], {'completed': 0, 'total': 1})
            all_ids = []
            for s in sections:
                for l in s['lessons']:
                    all_ids.append(l['id'])
            completed_lessons = all_ids[:prog['completed']]

    if not course:
        flash('Course not found.', 'error')
        return redirect(url_for('student.dashboard'))

    total = sum(len(s.get('lessons', [])) for s in sections)

    return render_template('student/progress.html', course=course,
                           sections=sections, completed_lessons=completed_lessons,
                           total_lessons=total,
                           completed_count=len(completed_lessons))


def _mock_enrolled():
    """Build mock enrolled-course list from COURSES + MOCK_PROGRESS."""
    result = []
    for cid in ENROLLED_IDS:
        c = next((x for x in COURSES if x['id'] == cid), None)
        if c:
            prog = MOCK_PROGRESS.get(cid, {'completed': 0, 'total': 1})
            result.append({**c, 'completed_lessons': prog['completed'],
                           'total_lessons': prog['total']})
    return result
