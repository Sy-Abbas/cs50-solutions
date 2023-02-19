import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
import datetime

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")
people = db.execute("SELECT name FROM birthdays where month = 10 and day = 24")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")

        if month != None and day!= None:
            months = int(month)
            days = int(day)
        else:
            return redirect("/")
        correctDate = None
        try:
            newDate = datetime.datetime(2020,months,days)
            correctDate = True
        except ValueError:
            correctDate = False


        if not name or correctDate == False:
            return redirect("/")
        db.execute("INSERT INTO birthdays (name, month, day) VALUES(?, ?, ?)", name, month, day)
        return redirect("/")

    else:
        people = db.execute("SELECT name FROM birthdays where month = 10 and day = 24")
        return render_template("index.html", people=people)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)