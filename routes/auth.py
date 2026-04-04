from flask import Blueprint,render_template,request,flash,redirect,url_for

auth=Blueprint('auth',__name__)

@auth.route("/sign-up",methods=('GET','POST'))
def sign_up():
    if request.method=='POST':
        email=request.form.get('email')
        userName=request.form.get('userName')
        password=request.form.get('password')
        password1=request.form.get('password1')

        if not email or not userName or not password or not password1:
            flash("Please fill in all fields.", category='error')
        
        elif len(userName) < 2:
            flash("Username is too short.", category='error')

        
        elif "@" not in email or "." not in email or email.count("@") > 1:
            flash("Please enter a valid email address.", category='error')

        elif len(password) < 7:
            flash("Password must be at least 7 characters.", category='error')

        elif password != password1:
            flash("Passwords do not match.", category='error')

        
        else:
            
            if "admin" in email.lower():
                flash("Welcome to the Admin Dashboard!", category='success')
                return redirect(url_for('admin.home')) 
            else:
                flash("Registration successful! Welcome, Student.", category='success')
                return redirect(url_for('student.home')) 

    return render_template("register.html")
@auth.route("/sign-in")
def sign_in():
    return "<p>sign in</p>"
    