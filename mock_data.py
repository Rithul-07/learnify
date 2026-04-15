"""
Mock data used when MySQL is not yet connected.
Delete this file once your database is live.
"""
import uuid
from datetime import datetime, timedelta

# ── CATEGORIES ───────────────────────────────────────────────
CATEGORIES = [
    {'id': 1, 'name': 'Web Development',  'slug': 'web-development',  'icon': '🌐'},
    {'id': 2, 'name': 'Python',           'slug': 'python',           'icon': '🐍'},
    {'id': 3, 'name': 'JavaScript',       'slug': 'javascript',       'icon': '⚡'},
    {'id': 4, 'name': 'Data Science',     'slug': 'data-science',     'icon': '📊'},
    {'id': 5, 'name': 'Mobile Dev',       'slug': 'mobile-dev',       'icon': '📱'},
    {'id': 6, 'name': 'DevOps',           'slug': 'devops',           'icon': '🔧'},
    {'id': 7, 'name': 'Databases',        'slug': 'databases',        'icon': '🗄️'},
    {'id': 8, 'name': 'UI/UX Design',     'slug': 'ui-ux-design',     'icon': '🎨'},
]

# ── COURSES ──────────────────────────────────────────────────
COURSES = [
    {
        'id': 1, 'title': 'HTML & CSS Foundations',
        'slug': 'html-css-foundations',
        'description': 'Master the building blocks of the web. Learn semantic HTML5, modern CSS3, Flexbox, Grid, responsive design, and accessibility best practices from the ground up.',
        'thumbnail': None, 'category_id': 1, 'category_name': 'Web Development',
        'category_icon': '🌐', 'level': 'beginner', 'status': 'published',
        'admin_id': 1, 'created_at': datetime.now() - timedelta(days=30),
        'total_lessons': 24, 'enrolled_count': 342,
    },
    {
        'id': 2, 'title': 'Python for Beginners',
        'slug': 'python-for-beginners',
        'description': 'Start your programming journey with Python. Cover variables, data types, control flow, functions, OOP, file handling, and build real-world projects.',
        'thumbnail': None, 'category_id': 2, 'category_name': 'Python',
        'category_icon': '🐍', 'level': 'beginner', 'status': 'published',
        'admin_id': 1, 'created_at': datetime.now() - timedelta(days=25),
        'total_lessons': 32, 'enrolled_count': 518,
    },
    {
        'id': 3, 'title': 'JavaScript Deep Dive',
        'slug': 'javascript-deep-dive',
        'description': 'Go beyond the basics. Closures, prototypes, async/await, event loop, ES6+ features, DOM manipulation, and modern JavaScript patterns explained clearly.',
        'thumbnail': None, 'category_id': 3, 'category_name': 'JavaScript',
        'category_icon': '⚡', 'level': 'intermediate', 'status': 'published',
        'admin_id': 1, 'created_at': datetime.now() - timedelta(days=20),
        'total_lessons': 28, 'enrolled_count': 276,
    },
    {
        'id': 4, 'title': 'Flask Web Development',
        'slug': 'flask-web-development',
        'description': 'Build production-grade web apps with Flask. Blueprints, Jinja2, SQLAlchemy, authentication, REST APIs, deployment, and best practices.',
        'thumbnail': None, 'category_id': 2, 'category_name': 'Python',
        'category_icon': '🐍', 'level': 'intermediate', 'status': 'published',
        'admin_id': 1, 'created_at': datetime.now() - timedelta(days=15),
        'total_lessons': 20, 'enrolled_count': 189,
    },
    {
        'id': 5, 'title': 'React & Modern Frontend',
        'slug': 'react-modern-frontend',
        'description': 'Learn React from scratch. Components, hooks, state management, routing, API integration, testing, and deploying single-page applications.',
        'thumbnail': None, 'category_id': 3, 'category_name': 'JavaScript',
        'category_icon': '⚡', 'level': 'advanced', 'status': 'published',
        'admin_id': 1, 'created_at': datetime.now() - timedelta(days=10),
        'total_lessons': 36, 'enrolled_count': 412,
    },
    {
        'id': 6, 'title': 'Data Science with Pandas',
        'slug': 'data-science-pandas',
        'description': 'Analyze real-world datasets with Python. Pandas, NumPy, data cleaning, visualization with Matplotlib & Seaborn, and exploratory data analysis.',
        'thumbnail': None, 'category_id': 4, 'category_name': 'Data Science',
        'category_icon': '📊', 'level': 'intermediate', 'status': 'published',
        'admin_id': 1, 'created_at': datetime.now() - timedelta(days=8),
        'total_lessons': 22, 'enrolled_count': 305,
    },
    {
        'id': 7, 'title': 'MySQL Masterclass',
        'slug': 'mysql-masterclass',
        'description': 'From CREATE TABLE to complex joins, subqueries, indexing, stored procedures, and database optimization. Become a confident SQL developer.',
        'thumbnail': None, 'category_id': 7, 'category_name': 'Databases',
        'category_icon': '🗄️', 'level': 'beginner', 'status': 'published',
        'admin_id': 1, 'created_at': datetime.now() - timedelta(days=5),
        'total_lessons': 18, 'enrolled_count': 154,
    },
    {
        'id': 8, 'title': 'Docker & Kubernetes',
        'slug': 'docker-kubernetes',
        'description': 'Containerize your applications and orchestrate at scale. Docker fundamentals, Compose, Kubernetes pods, services, deployments, and Helm charts.',
        'thumbnail': None, 'category_id': 6, 'category_name': 'DevOps',
        'category_icon': '🔧', 'level': 'advanced', 'status': 'published',
        'admin_id': 1, 'created_at': datetime.now() - timedelta(days=3),
        'total_lessons': 26, 'enrolled_count': 198,
    },
    {
        'id': 9, 'title': 'UI/UX Design Principles',
        'slug': 'ui-ux-design-principles',
        'description': 'Design interfaces people love. Color theory, typography, layout, wireframing, prototyping with Figma, user research, and usability testing.',
        'thumbnail': None, 'category_id': 8, 'category_name': 'UI/UX Design',
        'category_icon': '🎨', 'level': 'beginner', 'status': 'published',
        'admin_id': 1, 'created_at': datetime.now() - timedelta(days=1),
        'total_lessons': 16, 'enrolled_count': 230,
    },
]


def get_course_sections(course_id):
    """Return mock sections with nested lessons for a given course."""
    sections_map = {
        1: [
            {'id': 1, 'title': 'Getting Started with HTML', 'position': 1, 'lessons': [
                {'id': 1, 'title': 'What is HTML?', 'duration': 12, 'position': 1},
                {'id': 2, 'title': 'Setting Up Your Editor', 'duration': 8, 'position': 2},
                {'id': 3, 'title': 'Your First Web Page', 'duration': 15, 'position': 3},
                {'id': 4, 'title': 'HTML Document Structure', 'duration': 10, 'position': 4},
            ]},
            {'id': 2, 'title': 'HTML Elements & Semantics', 'position': 2, 'lessons': [
                {'id': 5, 'title': 'Text Elements & Headings', 'duration': 14, 'position': 1},
                {'id': 6, 'title': 'Links and Navigation', 'duration': 11, 'position': 2},
                {'id': 7, 'title': 'Images and Media', 'duration': 13, 'position': 3},
                {'id': 8, 'title': 'Semantic HTML5 Tags', 'duration': 16, 'position': 4},
            ]},
            {'id': 3, 'title': 'CSS Fundamentals', 'position': 3, 'lessons': [
                {'id': 9, 'title': 'Introduction to CSS', 'duration': 12, 'position': 1},
                {'id': 10, 'title': 'Selectors & Specificity', 'duration': 18, 'position': 2},
                {'id': 11, 'title': 'The Box Model', 'duration': 15, 'position': 3},
                {'id': 12, 'title': 'Colors & Typography', 'duration': 14, 'position': 4},
            ]},
            {'id': 4, 'title': 'Modern Layouts', 'position': 4, 'lessons': [
                {'id': 13, 'title': 'Flexbox Deep Dive', 'duration': 22, 'position': 1},
                {'id': 14, 'title': 'CSS Grid Mastery', 'duration': 25, 'position': 2},
                {'id': 15, 'title': 'Responsive Design', 'duration': 20, 'position': 3},
                {'id': 16, 'title': 'Media Queries', 'duration': 14, 'position': 4},
            ]},
        ],
    }
    # Fallback generic sections for courses not explicitly defined
    default = [
        {'id': 100, 'title': 'Introduction', 'position': 1, 'lessons': [
            {'id': 200, 'title': 'Welcome & Course Overview', 'duration': 10, 'position': 1},
            {'id': 201, 'title': 'Setting Up Your Environment', 'duration': 15, 'position': 2},
            {'id': 202, 'title': 'Key Concepts Overview', 'duration': 12, 'position': 3},
        ]},
        {'id': 101, 'title': 'Core Concepts', 'position': 2, 'lessons': [
            {'id': 203, 'title': 'Fundamentals Part 1', 'duration': 20, 'position': 1},
            {'id': 204, 'title': 'Fundamentals Part 2', 'duration': 18, 'position': 2},
            {'id': 205, 'title': 'Hands-On Practice', 'duration': 25, 'position': 3},
            {'id': 206, 'title': 'Common Patterns', 'duration': 22, 'position': 4},
        ]},
        {'id': 102, 'title': 'Advanced Topics', 'position': 3, 'lessons': [
            {'id': 207, 'title': 'Advanced Techniques', 'duration': 20, 'position': 1},
            {'id': 208, 'title': 'Best Practices', 'duration': 16, 'position': 2},
            {'id': 209, 'title': 'Real-World Project', 'duration': 30, 'position': 3},
        ]},
        {'id': 103, 'title': 'Final Project', 'position': 4, 'lessons': [
            {'id': 210, 'title': 'Project Planning', 'duration': 15, 'position': 1},
            {'id': 211, 'title': 'Building the Project', 'duration': 35, 'position': 2},
            {'id': 212, 'title': 'Review & Next Steps', 'duration': 10, 'position': 3},
        ]},
    ]
    return sections_map.get(course_id, default)


# ── MOCK ENROLLED COURSES (for student with id=2) ───────────
ENROLLED_IDS = [1, 2, 3]

MOCK_PROGRESS = {
    1: {'completed': 10, 'total': 16},
    2: {'completed': 5,  'total': 32},
    3: {'completed': 28, 'total': 28},
}

MOCK_CERTIFICATES = [
    {
        'id': 1, 'course_title': 'JavaScript Deep Dive',
        'issued_at': datetime.now() - timedelta(days=2),
        'cert_code': 'LRFY-' + uuid.uuid4().hex[:8].upper(),
    },
]

# ── MOCK USERS (for admin manage students) ──────────────────
MOCK_USERS = [
    {'id': 2, 'username': 'janedoe', 'email': 'jane@example.com',
     'full_name': 'Jane Doe', 'role': 'student', 'is_active': 1,
     'created_at': datetime.now() - timedelta(days=45)},
    {'id': 3, 'username': 'bobsmith', 'email': 'bob@example.com',
     'full_name': 'Bob Smith', 'role': 'student', 'is_active': 1,
     'created_at': datetime.now() - timedelta(days=30)},
    {'id': 4, 'username': 'alice_w', 'email': 'alice@example.com',
     'full_name': 'Alice Wang', 'role': 'student', 'is_active': 0,
     'created_at': datetime.now() - timedelta(days=22)},
    {'id': 5, 'username': 'charlie', 'email': 'charlie@example.com',
     'full_name': 'Charlie Brown', 'role': 'student', 'is_active': 1,
     'created_at': datetime.now() - timedelta(days=15)},
    {'id': 6, 'username': 'diana_p', 'email': 'diana@example.com',
     'full_name': 'Diana Prince', 'role': 'student', 'is_active': 1,
     'created_at': datetime.now() - timedelta(days=7)},
]

MOCK_ENROLLMENTS = [
    {'user': 'Jane Doe', 'course': 'HTML & CSS Foundations',
     'enrolled_at': datetime.now() - timedelta(days=40)},
    {'user': 'Jane Doe', 'course': 'Python for Beginners',
     'enrolled_at': datetime.now() - timedelta(days=38)},
    {'user': 'Bob Smith', 'course': 'JavaScript Deep Dive',
     'enrolled_at': datetime.now() - timedelta(days=28)},
    {'user': 'Alice Wang', 'course': 'Flask Web Development',
     'enrolled_at': datetime.now() - timedelta(days=20)},
    {'user': 'Charlie Brown', 'course': 'React & Modern Frontend',
     'enrolled_at': datetime.now() - timedelta(days=12)},
    {'user': 'Diana Prince', 'course': 'Data Science with Pandas',
     'enrolled_at': datetime.now() - timedelta(days=5)},
    {'user': 'Bob Smith', 'course': 'HTML & CSS Foundations',
     'enrolled_at': datetime.now() - timedelta(days=3)},
    {'user': 'Charlie Brown', 'course': 'MySQL Masterclass',
     'enrolled_at': datetime.now() - timedelta(days=1)},
]
