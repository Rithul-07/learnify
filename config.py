import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'learnify-dev-secret-key-2026')

    # Admin registration secret
    ADMIN_SECRET_KEY = os.environ.get('ADMIN_SECRET_KEY', 'learnify-admin-secret')

    # MySQL settings
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'your_password_here')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'learnify')
    MYSQL_CURSORCLASS = 'DictCursor'

    # Session
    SESSION_PERMANENT = False
    SESSION_TYPE = 'filesystem'