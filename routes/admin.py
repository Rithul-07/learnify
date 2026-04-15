import re
from flask import (Blueprint, render_template, request, redirect,
                   url_for, flash, session, current_app)
from routes import admin_required
from mock_data import (COURSES, CATEGORIES, MOCK_USERS,
                       MOCK_ENROLLMENTS)

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    stats = {}
    recent_enrollments = []

    if current_app.config.get('MYSQL_AVAILABLE'):
        try:
            cur = current_app.mysql.connection.cursor()
            cur.execute('SELECT COUNT(*) AS cnt FROM users WHERE role="student"')
            stats['students'] = cur.fetchone()['cnt']
            cur.execute('SELECT COUNT(*) AS cnt FROM courses')
            stats['courses'] = cur.fetchone()['cnt']
            cur.execute('SELECT COUNT(*) AS cnt FROM enrollments')
            stats['enrollments'] = cur.fetchone()['cnt']
            cur.execute('SELECT COUNT(*) AS cnt FROM certificates')
            stats['certificates'] = cur.fetchone()['cnt']
            cur.execute('''
                SELECT u.full_name AS user, c.title AS course, e.enrolled_at
                FROM enrollments e
                JOIN users u ON e.user_id = u.id
                JOIN courses c ON e.course_id = c.id
                ORDER BY e.enrolled_at DESC LIMIT 10
            ''')
            recent_enrollments = cur.fetchall()
            cur.close()
        except Exception:
            stats = _mock_stats()
            recent_enrollments = MOCK_ENROLLMENTS
    else:
        stats = _mock_stats()
        recent_enrollments = MOCK_ENROLLMENTS

    return render_template('admin/dashboard.html', stats=stats,
                           recent_enrollments=recent_enrollments)


@admin_bp.route('/post-course', methods=['GET', 'POST'])
@admin_required
def post_course():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        category_id = request.form.get('category_id', type=int)
        level = request.form.get('level', 'beginner')
        status = request.form.get('status', 'draft')

        if not title or not description:
            flash('Title and description are required.', 'error')
            return redirect(url_for('admin.post_course'))

        slug = _slugify(title)

        if current_app.config.get('MYSQL_AVAILABLE'):
            try:
                cur = current_app.mysql.connection.cursor()
                cur.execute('''
                    INSERT INTO courses (title, slug, description, category_id, level, status, admin_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                ''', (title, slug, description, category_id, level, status, session['user_id']))
                course_id = cur.lastrowid

                # ── Dynamic sections & lessons ──────────────
                sec_idx = 0
                while True:
                    sec_title = request.form.get(f'section_title_{sec_idx}')
                    if not sec_title:
                        break
                    cur.execute('''
                        INSERT INTO sections (course_id, title, position)
                        VALUES (%s, %s, %s)
                    ''', (course_id, sec_title.strip(), sec_idx))
                    section_id = cur.lastrowid

                    les_idx = 0
                    while True:
                        les_title = request.form.get(f'lesson_title_{sec_idx}_{les_idx}')
                        if not les_title:
                            break
                        les_content = request.form.get(f'lesson_content_{sec_idx}_{les_idx}', '')
                        les_video = request.form.get(f'lesson_video_{sec_idx}_{les_idx}', '')
                        les_duration = request.form.get(f'lesson_duration_{sec_idx}_{les_idx}', 0, type=int)
                        cur.execute('''
                            INSERT INTO lessons (section_id, course_id, title, content, video_url, duration, position)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ''', (section_id, course_id, les_title.strip(),
                              les_content, les_video, les_duration, les_idx))
                        les_idx += 1
                    sec_idx += 1

                current_app.mysql.connection.commit()
                cur.close()
                flash('Course created successfully!', 'success')
                return redirect(url_for('admin.dashboard'))
            except Exception as e:
                flash(f'Error creating course: {e}', 'error')
                return redirect(url_for('admin.post_course'))
        else:
            flash('Course created successfully! (demo mode)', 'success')
            return redirect(url_for('admin.dashboard'))

    # GET — load categories
    categories = CATEGORIES
    if current_app.config.get('MYSQL_AVAILABLE'):
        try:
            cur = current_app.mysql.connection.cursor()
            cur.execute('SELECT * FROM categories ORDER BY name')
            categories = cur.fetchall()
            cur.close()
        except Exception:
            pass

    return render_template('admin/post_course.html', categories=categories)


@admin_bp.route('/manage-students')
@admin_required
def manage_students():
    users = []
    if current_app.config.get('MYSQL_AVAILABLE'):
        try:
            cur = current_app.mysql.connection.cursor()
            cur.execute('SELECT * FROM users ORDER BY created_at DESC')
            users = cur.fetchall()
            cur.close()
        except Exception:
            users = MOCK_USERS
    else:
        users = MOCK_USERS

    return render_template('admin/manage_students.html', users=users)


@admin_bp.route('/toggle-user/<int:user_id>', methods=['POST'])
@admin_required
def toggle_user(user_id):
    if current_app.config.get('MYSQL_AVAILABLE'):
        try:
            cur = current_app.mysql.connection.cursor()
            cur.execute('SELECT is_active FROM users WHERE id=%s', (user_id,))
            user = cur.fetchone()
            if user:
                new_status = 0 if user['is_active'] else 1
                cur.execute('UPDATE users SET is_active=%s WHERE id=%s',
                            (new_status, user_id))
                current_app.mysql.connection.commit()
                flash('User status updated.', 'success')
            cur.close()
        except Exception as e:
            flash(f'Error: {e}', 'error')
    else:
        flash('User status toggled! (demo mode)', 'success')
    return redirect(url_for('admin.manage_students'))


@admin_bp.route('/delete-user/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    if user_id == session.get('user_id'):
        flash('You cannot delete yourself.', 'error')
        return redirect(url_for('admin.manage_students'))

    if current_app.config.get('MYSQL_AVAILABLE'):
        try:
            cur = current_app.mysql.connection.cursor()
            cur.execute('DELETE FROM users WHERE id=%s', (user_id,))
            current_app.mysql.connection.commit()
            cur.close()
            flash('User deleted.', 'success')
        except Exception as e:
            flash(f'Error: {e}', 'error')
    else:
        flash('User deleted! (demo mode)', 'success')
    return redirect(url_for('admin.manage_students'))


@admin_bp.route('/delete-course/<int:course_id>', methods=['POST'])
@admin_required
def delete_course(course_id):
    if current_app.config.get('MYSQL_AVAILABLE'):
        try:
            cur = current_app.mysql.connection.cursor()
            cur.execute('DELETE FROM courses WHERE id=%s', (course_id,))
            current_app.mysql.connection.commit()
            cur.close()
            flash('Course deleted.', 'success')
        except Exception as e:
            flash(f'Error: {e}', 'error')
    else:
        flash('Course deleted! (demo mode)', 'success')
    return redirect(url_for('admin.dashboard'))


def _slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    return re.sub(r'[-\s]+', '-', text)


def _mock_stats():
    return {
        'students': len(MOCK_USERS),
        'courses': len(COURSES),
        'enrollments': len(MOCK_ENROLLMENTS),
        'certificates': 3,
    }
