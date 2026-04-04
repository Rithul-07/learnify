import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'learnify-dev-secret-123')
    
    # MySQL settings — update these once MySQL is installed
    MYSQL_HOST     = 'localhost'
    MYSQL_USER     = 'root'
    MYSQL_PASSWORD = 'your_mysql_password'
    MYSQL_DB       = 'learnify'
    MYSQL_CURSORCLASS = 'DictCursor'