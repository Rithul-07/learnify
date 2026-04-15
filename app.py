import os

from flask import Flask
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ── Try to initialize MySQL ──────────────────────────────
    app.config['MYSQL_AVAILABLE'] = False
    app.mysql = None
    
    try:
        from flask_mysqldb import MySQL
        import MySQLdb
        
        # Test connection once at startup
        test_conn = MySQLdb.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            passwd=app.config['MYSQL_PASSWORD'],
            db=app.config['MYSQL_DB'],
            connect_timeout=2
        )
        test_conn.close()
        
        mysql = MySQL(app)
        app.mysql = mysql
        app.config['MYSQL_AVAILABLE'] = True
        print("MySQL connected successfully.")
    except Exception as e:
        print(f"MySQL connection failed: {e}. Falling back to Mock Mode.")
        app.config['MYSQL_AVAILABLE'] = False
        app.mysql = None

    # ── Register Blueprints ──────────────────────────────────
    from routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from routes.views import views_bp
    app.register_blueprint(views_bp)

    from routes.courses import courses_bp
    app.register_blueprint(courses_bp)

    from routes.student import student_bp
    app.register_blueprint(student_bp)

    from routes.admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # ── Jinja2 context processor ─────────────────────────────
    @app.context_processor
    def inject_now():
        from datetime import datetime
        return {'now': datetime.utcnow()}

    return app


app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', '5000'))
    app.run(debug=True, use_reloader=False, port=port)
