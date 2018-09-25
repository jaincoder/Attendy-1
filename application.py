from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
import numpy
import flask_mail
from datetime import datetime, date
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
import os 
import time
import calendar
from v0 import *
from flask import send_file

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"


Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///elo.db")



@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        # Ensure username was submitted
        trial = int(db.execute("SELECT Trial FROM ':i - Attendance' WHERE ID = :z", z = 1, i = session["user_id"])[0]["Trial"])
        if request.form.get("code") and trial == 0:
            user = request.form.get("code")
            password = str(db.execute("SELECT Password FROM ':i - Attendance' WHERE ID = :z", z = 1, i = session["user_id"])[0]["Password"])
            class_password = str(db.execute("SELECT Password FROM 'Admin' WHERE ID = :z", z = 1)[0]["Password"])
            time_started = db.execute("SELECT Time FROM ':i - Attendance' WHERE ID = :z", z = 1, i = session["user_id"])[0]["Time"]
            time_sent = calendar.timegm(time.gmtime())
            class_time = db.execute("SELECT Time FROM 'Admin' WHERE ID = :z", z = 1)[0]["Time"]
            display = class_password + password
            
            if round(int(time_sent) - int(time_started)) > 10 or round(int(time_sent) - int(class_time)) > 20: 
                return render_template("closed.html")
            
            if check1(6, 10, user, display) == 1:
                attendance = "Absent"
                return render_template("index.html", password = display, attendance = attendance)
            elif check1(6, 10, user, display) == 2:
                attendance = "Marked as Present"
                names = str(db.execute("SELECT Names FROM 'Admin' WHERE ID = :z", z = 1)[0]["Names"])
                names_list = names.split(",")
                names_list += [(db.execute("SELECT Name FROM ':i - Attendance' WHERE ID = :z", z = 1, i = session["user_id"])[0]["Name"])]
                names_list = list(set(names_list))
                names = ", ".join(str(name) for name in names_list)
                db.execute("UPDATE 'Admin' SET Names = :n WHERE ID = :z", n = names, z = 1)
                return render_template("index.html", password = display, attendance = attendance)
            else:
                display = ""
                if round(int(time_sent) - int(time_started)) < 10 and round(int(time_sent) - int(class_time)) < 20:
                    attendance = "Keep Trying"
                    trial += 1
                    db.execute("UPDATE ':i - Attendance' SET Trial = :t WHERE ID = :z", z = 1, i = session["user_id"], t = trial)
                else:
                    attendance = "Absent"
                return render_template("index.html", password = display, attendance = attendance)
        if request.form.get("code") and trial == 1:
            user = request.form.get("code")
            password = str(db.execute("SELECT Password FROM ':i - Attendance' WHERE ID = :z", z = 1, i = session["user_id"])[0]["Password"])
            class_password = str(db.execute("SELECT Password FROM 'Admin' WHERE ID = :z", z = 1)[0]["Password"])
            time_started = db.execute("SELECT Time FROM ':i - Attendance' WHERE ID = :z", z = 1, i = session["user_id"])[0]["Time"]
            time_sent = calendar.timegm(time.gmtime())
            class_time = db.execute("SELECT Time FROM 'Admin' WHERE ID = :z", z = 1)[0]["Time"]
            display = class_password + password
                    
            if check2(6, 5, user, display) and round(int(time_sent) - int(time_started)) < 20 and round(int(time_sent) - int(class_time)) < 30:
                attendance = "Keep Trying"
                trial += 1
                db.execute("UPDATE ':i - Attendance' SET Trial = :t WHERE ID = :z", z = 1, i = session["user_id"], t = trial)
                display = code_generator(3)[0]
                db.execute("UPDATE ':i - Attendance' SET Password = :p WHERE ID = :z", i = session["user_id"], p = display, z = 1)
                display = class_password + display
                return render_template("index.html", password = display, attendance = attendance)
            else:
                attendance = "Absent"
                db.execute("UPDATE ':i - Attendance' SET Trial = :t WHERE ID = :z", z = 1, i = session["user_id"], t = 0)
                return render_template("index.html", password = display, attendance = attendance)
        if request.form.get("code") and trial == 2:
            user = request.form.get("code")
            password = str(db.execute("SELECT Password FROM ':i - Attendance' WHERE ID = :z", z = 1, i = session["user_id"])[0]["Password"])
            class_password = str(db.execute("SELECT Password FROM 'Admin' WHERE ID = :z", z = 1)[0]["Password"])
            time_started = db.execute("SELECT Time FROM ':i - Attendance' WHERE ID = :z", z = 1, i = session["user_id"])[0]["Time"]
            time_sent = calendar.timegm(time.gmtime())
            class_time = db.execute("SELECT Time FROM 'Admin' WHERE ID = :z", z = 1)[0]["Time"]
            display = class_password + password
            db.execute("UPDATE ':i - Attendance' SET Trial = :t WHERE ID = :z", z = 1, i = session["user_id"], t = 0)
            if check3(6, 5, user, display) and round(int(time_sent) - int(time_started)) < 30 and round(int(time_sent) - int(class_time)) < 40:
                attendance = "Present"
                return render_template("index.html", password = display, attendance = attendance)
            else:
                attendance = "Absent"
                return render_template("index.html", password = display, attendance = attendance)

    
            
    now = calendar.timegm(time.gmtime())
    db.execute("UPDATE ':i - Attendance' SET Time = :t WHERE ID = :z", i = session["user_id"], z = 1, t = now)
    class_time = db.execute("SELECT Time FROM 'Admin' WHERE ID = :z", z = 1)[0]["Time"]
    
    
    if round(int(now) - int(class_time)) > 20:
        return render_template("closed.html")
    a = numpy.asarray([ [1,2,3], [4,5,6], [7,8,9] ])
    numpy.savetxt("foo.csv", a, delimiter=",")
    
    passwords = code_generator(3)
    password = passwords[0]
    db.execute("UPDATE ':i - Attendance' SET Password = :p WHERE ID = :z", i = session["user_id"], p = password, z = 1)
    
    
    
    attendance = "Undetermined"
    class_password = str(db.execute("SELECT Password FROM 'Admin' WHERE ID = :z", z = 1)[0]["Password"])
    password = str(class_password) + str(password)
    return render_template("index.html", password = password, attendance = attendance)


@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    if request.method == "POST":
        class_password = code_generator(3)[0]
        db.execute("UPDATE 'Admin' SET Password = :p WHERE ID = :z", p = class_password, z = 1)
        now = calendar.timegm(time.gmtime())
        db.execute("UPDATE 'Admin' SET Time = :t WHERE ID = :z", z = 1, t = now)
        test = db.execute("SELECT Password FROM 'Admin' WHERE ID = :z", z = 1)[0]["Password"]
        db.execute("UPDATE 'Admin' SET Names = :n WHERE ID = :z", n = "", z = 1)
        information = str(db.execute("SELECT Names FROM 'Admin' WHERE ID = :z", z = 1)[0]["Names"])
        return render_template("admin.html", test = test, information = information)
    test = db.execute("SELECT Password FROM 'Admin' WHERE ID = :z", z = 1)[0]["Password"]
    information = str(db.execute("SELECT Names FROM 'Admin' WHERE ID = :z", z = 1)[0]["Names"])
    return render_template("admin.html", test = test, information = information)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        if rows[0]["username"] == 'admin':
            return redirect("/admin")

        else:
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear() 

    # Redirect user to login form
    return redirect("/")




@app.route("/register", methods=["GET", "POST"])
def register():

    
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password", 403)

        # Ensure password was confirmed
        elif not request.form.get("confirmation"):
            return apology("Must provide confirmation", 403)

        if not (request.form.get("password") == request.form.get("confirmation")):
            return apology("Your password and password confirmation do not match", 403)

        hash_password = generate_password_hash(request.form.get("password"))

        # Query database for username
        result = db.execute("INSERT INTO users (username, hash) VALUES (:u, :p)", u = request.form.get("username"), p = hash_password)

        if not result:
            return apology("Sorry, but that username is taken", 403)

        id = db.execute("SELECT id FROM users WHERE username = :u", u = request.form.get("username"))
        if request.form.get("username") == "admin":
            db.execute("CREATE TABLE 'Admin' ('ID' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'Password' TEXT NOT NULL, 'Time' NUMERIC NOT NULL, 'Names' TEXT NOT NULL)")
            db.execute("INSERT INTO 'Admin' (Password, Time, Names) VALUES (:p, :t, :n)", p = "initial", t = 0, n = "")
            session["user_id"] = id[0]["id"]
            return redirect("/admin")
        else:
            db.execute("CREATE TABLE ':i - Attendance' ('ID' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'Name' TEXT NOT NULL, 'Password' TEXT NOT NULL, 'Time' NUMERIC NOT NULL, 'Trial' NUMERIC NOT NULL)", i = id[0]["id"])
            db.execute("INSERT INTO ':i - Attendance' (Name, Password, Time, Trial) VALUES (:n, :p, :t, :l)", n = str(request.form.get("username")), i = id[0]["id"], p = "initial", t = 0, l = 0)


        session["user_id"] = id[0]["id"]

        # Redirect user to home page
        flash('Registered!')
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")



@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password", 403)

        # Ensure password was confirmed
        elif not request.form.get("confirmation"):
            return apology("Must provide confirmation", 403)

        if not (request.form.get("password") == request.form.get("confirmation")):
            return apology("Your password and password confirmation do not match", 403)

        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
        if len(rows) != 1:
            return apology("This username does not exist", 403)


        hash_password = generate_password_hash(request.form.get("password"))

        result = db.execute("UPDATE users SET hash = :h WHERE ID = :i", i = session["user_id"], h = hash_password)
        # Redirect user to home page
        flash('Password Changed!')
        return redirect("/")

    else:
        return render_template("change_password.html")



def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
