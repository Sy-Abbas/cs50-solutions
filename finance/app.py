import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date
from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")
username = "Abbas"

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
    data1 = db.execute("SELECT nameofstock, shares, boughtat FROM user_shares_records WHERE username = ?", username)

    # Calculating total number of shares for each stock
    dicts = {}
    for x in range(len(data1)):
        if (data1[x]["nameofstock"] not in dicts.keys()):
            dicts[data1[x]["nameofstock"]] = 0
        dicts[data1[x]["nameofstock"]] += data1[x]["shares"]

    # Storing Data to Display
    datas = []
    total = 0
    for key, value in dicts.items():
        symbol = db.execute("SELECT symbol FROM user_shares_records WHERE nameofstock = ?", key)[0]["symbol"]
        price = lookup(symbol)["price"]
        shares = db.execute("SELECT shares FROM user_shares WHERE username = ? and symbol = ?", username, symbol)[0]["shares"]
        totalValue = price*shares
        total += totalValue

        dataDict = {}
        dataDict["stockSymbol"] = symbol
        dataDict["stockName"] = key
        dataDict["shares"] = shares
        dataDict["currentPrice"] = usd(price)
        dataDict["totalValue"] = usd(totalValue)

        datas.append(dataDict)

    # Displaying Updated Data
    userMoney = int(db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"])
    total += userMoney
    finaldata = {"currentCash": usd(userMoney), "totalMoney": usd(total)}

    return render_template("index.html", datas=datas, finaldata=finaldata)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("shares must be a posative integer", 400)
        # Form Input Validation
        if not symbol:
            return apology("Must provide symbol", 400)
        elif not shares:
            return apology("Must provide number of shares", 400)
        elif int(shares) < 1:
            return apology("Number of shares should be positive", 400)
        elif lookup(symbol) == None:
            return apology("Invalid Symbol", 400)

        # Can the user buy that stock, if so update the user's money
        price = lookup(symbol)["price"]
        userMoney = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        if int(userMoney) < (float(price) * int(shares)):
            return apology(f"You can buy {shares} number of {symbol} shares", 400)
        userMoney = userMoney - (price * int(shares))
        db.execute("UPDATE users SET cash = ? WHERE id = ?", userMoney, session["user_id"])

        # Add user bought shares to a table
        username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
        today = date.today()
        stockName = lookup(symbol)["name"]
        db.execute("INSERT INTO user_shares_records (username, symbol, nameofstock, shares, boughtat, date, action) VALUES(?, ?, ?, ?, ?, ?, ?)",
                   username, symbol, stockName, shares, price, today, "Buy")
        currentshares = db.execute("SELECT shares FROM user_shares WHERE username = ? and symbol = ?", username, symbol)
        if (len(currentshares)) == 0:
            db.execute("INSERT INTO user_shares (username, symbol, shares) VALUES(?, ?, ?)", username, symbol, shares)
        else:
            newshares = int(currentshares[0][shares]) + shares
            db.execute("UPDATE user_shares SET shares = ? WHERE username = ? and symbol = ?", newshares, username, symbol)
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
    data = db.execute("SELECT symbol, nameofstock, shares, boughtat, date, action FROM user_shares_records WHERE username = ?", username)
    datas = []
    for dicts in data:
        newlist = []
        newlist.append(dicts["symbol"])
        newlist.append(dicts["nameofstock"])
        newlist.append(dicts["action"])
        newlist.append(dicts["shares"])
        newlist.append(usd(dicts["boughtat"]))
        newlist.append(dicts["date"])

        datas.append(newlist)
    return render_template("history.html", datas=datas)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Must provide symbol", 400)

        dicts = lookup(symbol)

        if dicts == None:
            return apology("No stock exists for this symbol")
        else:
            datas = [dicts["name"], usd(dicts["price"]), dicts["symbol"]]
            return render_template("quoted.html", datas=datas)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        cpassword = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            return apology("Must provide username", 400)

        # Ensure password and confirmed was submitted
        elif not password:
            return apology("Must provide password", 400)

        elif not cpassword:
            return apology("Must confirm password", 400)

        # Ensure username doesn't exists
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 0:
            return apology("The username already exists.")

        # Ensure the password entered is same
        if password != cpassword:
            return apology("passwords don't match", 400)

        # Register the user to the database
        phash = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, phash)

        # Remember which user has logged in
        user = db.execute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = user[0]["id"]

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]

    if request.method == "POST":
        symbol = request.form.get("symbol")
        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("shares must be a posative integer", 400)
        # Form Input Validation
        if not symbol:
            return apology("Must provide symbol", 400)
        elif not shares:
            return apology("Must provide number of shares", 400)
        elif int(shares) < 1:
            return apology("Number of shares should be positive", 400)
        elif lookup(symbol) == None:
            return apology("Invalid Symbol", 400)
        numberofshare = db.execute("SELECT shares FROM user_shares WHERE username = ? and symbol = ?",
                                   username, symbol)[0]["shares"]
        if shares > numberofshare:
            return apology("You dont have that many stocks to sell", 400)

        # Update number of shares
        newshares = numberofshare - shares
        db.execute("UPDATE user_shares SET shares = ? WHERE username = ? and symbol = ?", newshares, username, symbol)

        # Update current cash
        price = lookup(symbol)["price"]
        moneymade = price*shares
        userMoney = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        newcash = float(userMoney) + float(moneymade)
        db.execute("UPDATE users SET cash = ? WHERE username = ?", newcash, username)

        # Add Sell Record
        today = date.today()
        stockName = lookup(symbol)["name"]
        db.execute("INSERT INTO user_shares_records (username, symbol, nameofstock, shares, boughtat, date, action) VALUES(?, ?, ?, ?, ?, ?, ?)",
                   username, symbol, stockName, shares, price, today, "Sell")
        return redirect("/")

    else:
        stockdata = db.execute("SELECT symbol, shares FROM user_shares WHERE username = ?", username)
        stocks = []
        for x in range(len(stockdata)):
            stocks.append(stockdata[x]["symbol"])
        return render_template("sell.html", stocks=stocks)


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)