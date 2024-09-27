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

@app.route('/admin/users', methods=["POST", "GET"])
def admin_users():
    if request.method == "POST":
        if not request.form.get("username"):
            flash("Must provide username")
            return render_template("admin_add.html")

        # Ensure password was submitted
        if not request.form.get("password"):
            flash("Must provide password")
            return render_template("admin_add.html")
        
        #Ensure role was submitted
        if not request.form.get("role"):
            flash("Must enter role")
            return render_template("admin_add.html")
        
        if request.form.get("role") not in ['Student', 'Professor']:
            flash("Invalid role")
            return render_template("admin_add.html")
        
        try:
            hashed_password = generate_password_hash(request.form.get("password"), "pbkdf2")
            db.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", 
                    request.form.get("username"),
                    hashed_password,
                    request.form.get("role")
                    )
            flash("User succesfully added")
        except ValueError:
            flash("User already exists")
            return render_template("admin_add.html")
        return render_template("admin_add.html")
    else:
        professors = db.execute("SELECT * FROM users WHERE role = 'Professor'")
        return render_template("admin_add.html", professors=professors)

@app.route('/admin/courses', methods=["GET", "POST"])
def admin_courses():
    if request.method == "POST":
        if not request.form.get("coursename"):
            flash("Must provide coursename")
            return render_template("admin_add.html")
        
        if not request.form.get("professor"):
            flash("Must provide professor's name")
            return render_template("admin_add.html")
        
        id = db.execute("SELECT id FROM users WHERE username = ?", request.form.get("professor"))
        db.execute("INSERT INTO courses (course_name, professor_id) VALUES (?, ?)", 
                   request.form.get("coursename"), id[0]["id"] )
        flash("Course succesfully added")
        return render_template("admin_add.html")

    else:
        professors = db.execute("SELECT * FROM users WHERE role = 'Professor'")
        return render_template("admin_add.html", professors=professors)

@app.route('/admin/manage', methods=['GET', 'POST'])
def admin_manage_users():
    users = db.execute("SELECT * FROM users WHERE role != 'Admin'")
    courses = db.execute("SELECT * FROM courses")
    return render_template("admin_view.html", users = users, courses = courses)

@app.route('/admin/manage/<user_id>', methods=["POST", "GET"])
def admin_remove_user(user_id):
    return f"User {user_id} removed"

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
            flash("Must provide username")
            return render_template("login.html")

        # Ensure password was submitted
        if not request.form.get("password"):
            flash("Must provide password")
            return render_template("login.html")
        
        #Ensure role was submitted
        if not request.form.get("role"):
            flash("Must enter role")
            return render_template("login.html")
        
        if request.form.get("role") in ['Admin', 'Students', 'Professor']:
            flash("Invalid role")
            return render_template("login.html")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or request.form.get('password') != rows[0]['password_hash']:
            flash("Incorrect password/username")
            return render_template("login.html")

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
