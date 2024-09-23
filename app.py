from flask import Flask, flash, redirect, render_template, request, session, jsonify
from cs50 import SQL
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///project.db")


@app.route('/')
def hello_world():
    return render_template("index.html")

#Admin routes
@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route('/admin/users')
def admin_users():
    return 'admin users'

@app.route('/admin/courses')
def admin_courses():
    return 'admin courses'

@app.route('/admin/create_user', methods=['GET', 'POST'])
def admin_create_users():
    return 'admin create users'

#Authentication Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    # """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("invalid.html", message='Must provide username')

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("invalid.html", message='Must provide password')
        
        #Ensure role was submitted
        elif not request.form.get("role"):
            return render_template("invalid.html", message='Must provide role')

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or request.form.get('password') != rows[0]['password_hash']:
            return "INVALID login"

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to appropriate page
        if(rows[0]['role'] == 'Admin'):
            return redirect("/admin")
        
        if(rows[0]['role'] == 'Professor'):
            return redirect("/professor/courses")
        
        if(rows[0]['role'] == 'Ptudent'):
            return redirect("/student/courses")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")



@app.route('/logout')
def logout():
    return 'logout page'

#Dashboard
@app.route("/dashboard")
def dashboard():
    return 'dashboard page'

#Students routes
@app.route("/student/courses")
def student_courses():
    return 'Student courses page'

@app.route("/student/courses/<course_id>")
def student_courses_id(course_id):
    return f'Courses {course_id}'

#Professor routes
@app.route("/professor/courses")
def professor_courses():
    return 'Student courses page'

@app.route("/professor/courses/<course_id>")
def professor_courses_id(course_id):
    return f'Courses {course_id}'

@app.route("/professor/courses/<course_id>/add_grade", methods=['GET', 'POST'])
def professor_courses_id_add(course_id):
    return f'Courses {course_id} added/edited'

if __name__ == "__main__":
    app.run(debug=True)
