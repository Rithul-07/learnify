"""Quick smoke-test for every route in the project."""
from app import create_app

app = create_app()
client = app.test_client()

errors = []

def check(label, resp):
    if resp.status_code == 200:
        print(f"  OK  {label}")
    else:
        msg = f"FAIL  {label} -> {resp.status_code}"
        print(msg)
        # Show the first line of the traceback if it's a 500
        if resp.status_code == 500:
            body = resp.data.decode("utf-8", errors="replace")
            for line in body.splitlines():
                if "Error" in line or "error" in line or "Traceback" in line:
                    msg += " | " + line.strip()
                    break
        errors.append(msg)

# ── Public pages ────────────────────────────────────────────
print("=== Public Pages ===")
check("Home /", client.get("/"))
check("Login /login", client.get("/login"))
check("Register /register", client.get("/register"))
check("Courses /courses", client.get("/courses"))
check("Course Detail", client.get("/courses/html-css-foundations"))
check("Course Detail 2", client.get("/courses/python-for-beginners"))

# ── Student pages ───────────────────────────────────────────
print("\n=== Student Pages ===")
with client.session_transaction() as sess:
    sess["user_id"] = 2
    sess["username"] = "student"
    sess["full_name"] = "Test Student"
    sess["role"] = "student"

check("Student Dashboard", client.get("/dashboard"))
check("Student Progress", client.get("/progress/html-css-foundations"))

# ── Admin pages ─────────────────────────────────────────────
print("\n=== Admin Pages ===")
with client.session_transaction() as sess:
    sess["user_id"] = 1
    sess["username"] = "admin"
    sess["full_name"] = "Admin User"
    sess["role"] = "admin"

check("Admin Dashboard", client.get("/admin/dashboard"))
check("Admin Manage Students", client.get("/admin/manage-students"))
check("Admin Post Course", client.get("/admin/post-course"))

# ── Summary ─────────────────────────────────────────────────
print("\n" + "=" * 40)
if errors:
    print(f"ERRORS: {len(errors)}")
    for e in errors:
        print(f"  {e}")
else:
    print("ALL PAGES PASSED!")
