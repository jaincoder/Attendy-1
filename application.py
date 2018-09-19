from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from datetime import datetime, date
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
import os 
from v0 import *


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
        if request.form.get("code"):
            user = request.form.get("code")
            if check1(6, 5, user, password) == 1:
                password = "fqeWrS"
                attendance = "Absent"
                return render_template("index.html", password = password, attendance = attendance)
            elif check1(6, 5, user, password) == 2:
                password = "fqeWrS"
                attendance = "Present"
                return render_template("index.html", password = password, attendance = attendance)
            else:
                attendance = "Keep Trying"
                password = "fqeWrS"
                return render_template("index.html", password = password, attendance = attendance)
                """first_pass += 1
            if request.form.get("code"):
            user = request.form.get("code")
            if check2(6, 5, user, password):
                attendance = "Keep Trying"
                return render_template("index.html", password = password, attendance = attendance)
            else:
                attendance = "Absent"
                return render_template("index.html", password = password, attendance = attendance)
        if first_pass == 3 and request.form.get("code"):
            user = request.form.get("code")
            if check3(6, 5, user, password):
                attendance = "Present"
                return render_template("index.html", password = password, attendance = attendance)
            else:
                attendance = "Absent"
                return render_template("index.html", password = password, attendance = attendance)
            first_pass = 1"""
    password = "fqeWrS"
    attendance = "Undetermined"
    return render_template("index.html", password = password, attendance = attendance)





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
        db.execute("CREATE TABLE ':i - Player Database' ('ID' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'Name' TEXT NOT NULL, 'Games Played' INTEGER NOT NULL, 'Rating' NUMERIC NOT NULL, 'Consistency' NUMERIC NOT NULL)", i = id[0]["id"])
        db.execute("CREATE TABLE ':i - Result History' ('ID' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'Player_A' TEXT NOT NULL, 'A_Change' NUMERIC NOT NULL, 'A_New_Rating' NUMERIC NOT NULL, 'A_Consistency' NUMERIC NOT NULL, 'Player_B' TEXT NOT NULL, 'B_Change' NUMERIC NOT NULL, 'B_New_Rating' NUMERIC NOT NULL, 'B_Consistency' NUMERIC NOT NULL, 'Result' NUMERIC NOT NULL, 'Timestamp' DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP)", i = id[0]["id"])


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
