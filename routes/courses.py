from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from routes import login_required
from mock_data import COURSES, CATEGORIES, get_course_sections, ENROLLED_IDS, MOCK_PROGRESS

courses_bp = Blueprint('courses', __name__)


@courses_bp.route('/courses')
def course_list():
    category_filter = request.args.get('category', '')
    level_filter = request.args.get('level', '')
    search_q = request.args.get('q', '').strip()
    sort_by = request.args.get('sort', 'newest')

    if current_app.config.get('MYSQL_AVAILABLE'):
        try:
            cur = current_app.mysql.connection.cursor()
            query = '''
                SELECT c.*, cat.name AS category_name, cat.icon AS category_icon,
                       (SELECT COUNT(*) FROM enrollments e WHERE e.course_id = c.id) AS enrolled_count,
                       (SELECT COUNT(*) FROM lessons l WHERE l.course_id = c.id) AS total_lessons
                FROM courses c
                LEFT JOIN categories cat ON c.category_id = cat.id
                WHERE c.status = 'published'
            '''
            params = []
            if category_filter:
                query += ' AND cat.slug = %s'
                params.append(category_filter)
            if level_filter:
                query += ' AND c.level = %s'
                params.append(level_filter)
            if search_q:
                query += ' AND (c.title LIKE %s OR c.description LIKE %s)'
                like = f'%{search_q}%'
                params.extend([like, like])
            if sort_by == 'popular':
                query += ' ORDER BY enrolled_count DESC'
            else:
                query += ' ORDER BY c.created_at DESC'
            cur.execute(query, params)
            courses = cur.fetchall()
            cur.execute('SELECT * FROM categories ORDER BY name')
            categories = cur.fetchall()
            cur.close()
        except Exception:
            courses = COURSES
            categories = CATEGORIES
    else:
        courses = list(COURSES)
        categories = CATEGORIES
        # Apply mock filters
        if category_filter:
            courses = [c for c in courses if
                       any(cat['slug'] == category_filter and cat['id'] == c['category_id']
                           for cat in categories)]
        if level_filter:
            courses = [c for c in courses if c['level'] == level_filter]
        if search_q:
            sq = search_q.lower()
            courses = [c for c in courses
                       if sq in c['title'].lower() or sq in c['description'].lower()]
        if sort_by == 'popular':
            courses.sort(key=lambda x: x.get('enrolled_count', 0), reverse=True)
        else:
            courses.sort(key=lambda x: x.get('created_at', ''), reverse=True)

    return render_template('courses.html', courses=courses, categories=categories,
                           category_filter=category_filter, level_filter=level_filter,
                           search_q=search_q, sort_by=sort_by)


@courses_bp.route('/courses/<slug>')
def course_detail(slug):
    course = None
    sections = []
    is_enrolled = False
    progress = {}
    completed_lessons = []

    if current_app.config.get('MYSQL_AVAILABLE'):
        try:
            cur = current_app.mysql.connection.cursor()
            cur.execute('''
                SELECT c.*, cat.name AS category_name, cat.icon AS category_icon,
                       (SELECT COUNT(*) FROM enrollments e WHERE e.course_id = c.id) AS enrolled_count,
                       (SELECT COUNT(*) FROM lessons l WHERE l.course_id = c.id) AS total_lessons
                FROM courses c
                LEFT JOIN categories cat ON c.category_id = cat.id
                WHERE c.slug = %s
            ''', (slug,))
            course = cur.fetchone()
            if course:
                cur.execute('''
                    SELECT * FROM sections WHERE course_id=%s ORDER BY position
                ''', (course['id'],))
                sections_raw = cur.fetchall()
                for sec in sections_raw:
                    cur.execute('''
                        SELECT * FROM lessons WHERE section_id=%s ORDER BY position
                    ''', (sec['id'],))
                    sec['lessons'] = cur.fetchall()
                sections = sections_raw

                if 'user_id' in session:
                    cur.execute('SELECT id FROM enrollments WHERE user_id=%s AND course_id=%s',
                                (session['user_id'], course['id']))
                    is_enrolled = cur.fetchone() is not None
                    if is_enrolled:
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
            if 'user_id' in session and course['id'] in ENROLLED_IDS:
                is_enrolled = True
                prog = MOCK_PROGRESS.get(course['id'], {'completed': 0, 'total': 1})
                # Mark first N lessons as completed
                all_lesson_ids = []
                for s in sections:
                    for l in s['lessons']:
                        all_lesson_ids.append(l['id'])
                completed_lessons = all_lesson_ids[:prog['completed']]

    if not course:
        flash('Course not found.', 'error')
        return redirect(url_for('courses.course_list'))

    # Calculate total lessons from sections
    total_lessons_count = sum(len(s.get('lessons', [])) for s in sections)
    completed_count = len(completed_lessons)

    return render_template('course_detail.html', course=course, sections=sections,
                           is_enrolled=is_enrolled,
                           completed_lessons=completed_lessons,
                           total_lessons=total_lessons_count,
                           completed_count=completed_count)


@courses_bp.route('/courses/<slug>/enroll', methods=['POST'])
@login_required
def enroll(slug):
    if current_app.config.get('MYSQL_AVAILABLE'):
        try:
            cur = current_app.mysql.connection.cursor()
            cur.execute('SELECT id FROM courses WHERE slug=%s', (slug,))
            course = cur.fetchone()
            if course:
                cur.execute('SELECT id FROM enrollments WHERE user_id=%s AND course_id=%s',
                            (session['user_id'], course['id']))
                if not cur.fetchone():
                    cur.execute('INSERT INTO enrollments (user_id, course_id) VALUES (%s,%s)',
                                (session['user_id'], course['id']))
                    current_app.mysql.connection.commit()
                    flash('Successfully enrolled!', 'success')
                else:
                    flash('You are already enrolled.', 'info')
            else:
                flash('Course not found.', 'error')
            cur.close()
        except Exception as e:
            flash(f'Enrollment error: {e}', 'error')
    else:
        flash('Successfully enrolled! (demo mode)', 'success')

    return redirect(url_for('courses.course_detail', slug=slug))


@courses_bp.route('/courses/<slug>/complete-lesson/<int:lesson_id>', methods=['POST'])
@login_required
def complete_lesson(slug, lesson_id):
    if current_app.config.get('MYSQL_AVAILABLE'):
        try:
            cur = current_app.mysql.connection.cursor()
            cur.execute('SELECT id FROM courses WHERE slug=%s', (slug,))
            course = cur.fetchone()
            if course:
                cur.execute('''
                    INSERT INTO lesson_progress (user_id, lesson_id, course_id, completed, completed_at)
                    VALUES (%s, %s, %s, 1, NOW())
                    ON DUPLICATE KEY UPDATE completed=1, completed_at=NOW()
                ''', (session['user_id'], lesson_id, course['id']))
                current_app.mysql.connection.commit()

                # Check if all lessons are completed — issue certificate
                cur.execute('SELECT COUNT(*) AS cnt FROM lessons WHERE course_id=%s',
                            (course['id'],))
                total = cur.fetchone()['cnt']
                cur.execute('''
                    SELECT COUNT(*) AS cnt FROM lesson_progress
                    WHERE user_id=%s AND course_id=%s AND completed=1
                ''', (session['user_id'], course['id']))
                done = cur.fetchone()['cnt']
                if done >= total and total > 0:
                    import uuid as _uuid
                    cert_code = 'LRFY-' + _uuid.uuid4().hex[:8].upper()
                    cur.execute('''
                        INSERT IGNORE INTO certificates (user_id, course_id, cert_code)
                        VALUES (%s, %s, %s)
                    ''', (session['user_id'], course['id'], cert_code))
                    cur.execute('''
                        UPDATE enrollments SET completed_at=NOW()
                        WHERE user_id=%s AND course_id=%s
                    ''', (session['user_id'], course['id']))
                    current_app.mysql.connection.commit()
                    flash('🎉 Congratulations! You completed this course and earned a certificate!', 'success')
            cur.close()
        except Exception as e:
            flash(f'Error: {e}', 'error')
    else:
        flash('Lesson marked complete! (demo mode)', 'success')

    return redirect(url_for('courses.course_detail', slug=slug))
