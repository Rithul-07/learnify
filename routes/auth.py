from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')
        admin_key = request.form.get('admin_key', '').strip()

        # ── Validation ──────────────────────────────────────
        if not all([full_name, username, email, password, confirm]):
            flash('Please fill in all fields.', 'error')
            return redirect(url_for('auth.register'))

        if len(username) < 3:
            flash('Username must be at least 3 characters.', 'error')
            return redirect(url_for('auth.register'))

        if '@' not in email or '.' not in email:
            flash('Please enter a valid email address.', 'error')
            return redirect(url_for('auth.register'))

        if len(password) < 7:
            flash('Password must be at least 7 characters.', 'error')
            return redirect(url_for('auth.register'))

        if password != confirm:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('auth.register'))

        # ── Determine role ──────────────────────────────────
        role = 'student'
        if admin_key:
            if admin_key == current_app.config.get('ADMIN_SECRET_KEY'):
                role = 'admin'
            else:
                flash('Invalid admin secret key.', 'error')
                return redirect(url_for('auth.register'))

        password_hash = generate_password_hash(password)

        # ── Database insert ─────────────────────────────────
        if current_app.config.get('MYSQL_AVAILABLE'):
            try:
                cur = current_app.mysql.connection.cursor()
                cur.execute('SELECT id FROM users WHERE email=%s OR username=%s',
                            (email, username))
                if cur.fetchone():
                    flash('Email or username already exists.', 'error')
                    return redirect(url_for('auth.register'))
                cur.execute(
                    '''INSERT INTO users
                       (username, email, password_hash, full_name, role)
                       VALUES (%s, %s, %s, %s, %s)''',
                    (username, email, password_hash, full_name, role)
                )
                current_app.mysql.connection.commit()
                cur.close()
            except Exception as e:
                flash(f'Registration error: {e}', 'error')
                return redirect(url_for('auth.register'))
        # (mock mode — no DB, just flash success)

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        if session.get('role') == 'admin':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('student.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not email or not password:
            flash('Please fill in all fields.', 'error')
            return redirect(url_for('auth.login'))

        user = None

        if current_app.config.get('MYSQL_AVAILABLE'):
            try:
                cur = current_app.mysql.connection.cursor()
                cur.execute('SELECT * FROM users WHERE email=%s', (email,))
                user = cur.fetchone()
                cur.close()
            except Exception:
                user = None

        if user:
            if not user.get('is_active'):
                flash('Your account has been deactivated. Contact admin.', 'error')
                return redirect(url_for('auth.login'))
            if check_password_hash(user['password_hash'], password):
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['full_name'] = user['full_name']
                session['role'] = user['role']
                flash(f'Welcome back, {user["full_name"]}!', 'success')
                if user['role'] == 'admin':
                    return redirect(url_for('admin.dashboard'))
                return redirect(url_for('student.dashboard'))
            else:
                flash('Invalid email or password.', 'error')
                return redirect(url_for('auth.login'))
        else:
            # ── Mock-login for demo (no DB) ─────────────────
            if not current_app.config.get('MYSQL_AVAILABLE'):
                if email == 'admin@learnify.com' and password == 'admin123':
                    session['user_id'] = 1
                    session['username'] = 'admin'
                    session['full_name'] = 'Admin User'
                    session['role'] = 'admin'
                    flash('Welcome back, Admin User!', 'success')
                    return redirect(url_for('admin.dashboard'))
                elif email and password:
                    session['user_id'] = 2
                    session['username'] = 'student'
                    session['full_name'] = email.split('@')[0].title()
                    session['role'] = 'student'
                    flash(f'Welcome back, {session["full_name"]}!', 'success')
                    return redirect(url_for('student.dashboard'))
            flash('Invalid email or password.', 'error')
            return redirect(url_for('auth.login'))

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('views.home'))