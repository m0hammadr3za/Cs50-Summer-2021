import os
import re

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    user_id = session["user_id"]
    user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = ?", user_id)

    # For each transaction of this user look up the symbol and add the name and the price to the transaction
    total_cash = user_cash
    for transaction in transactions:
        qoute = lookup(transaction["symbol"])
        transaction["name"] = qoute["name"]
        transaction["price"] = qoute["price"]
        total_cash += transaction["price"] * transaction["shares"]

    return render_template("index.html", total_cash=total_cash, user_cash=user_cash, transactions=transactions)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":
        # Error handling form inputs
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Please enter a symbol!")

        shares = request.form.get("shares")
        if not shares:
            return apology("Please enter the number of shares!")

        shares = int(shares)
        if not shares > 0:
            return apology("Please enter a positive number greater than 0!")

        # Check to see if symbol is a valid symbol
        qoute = lookup(symbol)
        if not qoute:
            return apology("Invalid symbol!")

        # Check to see if the user has enough cash in their account
        user_id = session["user_id"]
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
        total_price = qoute["price"] * shares
        if user_cash < total_price:
            return apology("You don't have enough cash for this purchase!")

        # Check if transaction already exists, if so update it, if not, create one
        transaction = db.execute("SELECT * FROM transactions WHERE user_id = ? AND symbol = ?", user_id, qoute["symbol"])
        if len(transaction) != 0:
            db.execute("UPDATE transactions SET shares = ? WHERE user_id = ? AND symbol = ?", transaction[0]["shares"] + shares, user_id, qoute["symbol"])
        else:
            db.execute("INSERT INTO transactions (user_id, symbol, shares) VALUES (?, ?, ?)", user_id, qoute["symbol"], shares)

        # Add transaction to the history of transactions and update user's cash
        db.execute("INSERT INTO histories (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)", user_id, qoute["symbol"], shares, qoute["price"])
        db.execute("UPDATE users SET cash = ? WHERE id = ?", (user_cash - total_price), user_id)

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Show all the transactions of this user on histories table
    user_id = session["user_id"]
    transactions = db.execute("SELECT * FROM histories WHERE user_id = ?", user_id)
    return render_template("history.html", transactions=transactions)


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
        # Error handling for form inputs
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Please enter a symbol!")

        # Check if symbol is a valid symbol
        quote = lookup(symbol)
        if not quote:
            return apology("Invalid symbol!")

        # show the qoute information
        return render_template("quoted.html", quote=quote)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        # Error handling for form inputs
        username = request.form.get("username")
        if not username:
            return apology("Please enter a username!")

        password = request.form.get("password")
        if not password:
            return apology("Please enter your password!")

        # Check to see if it's a safe password
        pattern = re.compile("(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])(?=.{8,})")
        match = re.search(pattern, password)
        if not match:
            return apology("Please enter a password that is at least 8 characters long, has at least 1 lowercase and 1 uppercase and 1 special character in it!")

        confirmation = request.form.get("confirmation")
        if not confirmation:
            return apology("Please enter your confirmation password!")

        if password != confirmation:
            return apology("Your passwords does not match! please try again.")

        # Check if user already exists
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 0:
            return apology("A user with this username already exists!")

        # Hash the password add the new user to the database
        hashed_password = generate_password_hash(password)
        user_id = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hashed_password)

        # Set the session with user's id and redirect to the homepage
        session["user_id"] = user_id
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # Get the list of symbols that this user has stock of them
    user_id = session["user_id"]
    symbols = []
    for symbol in db.execute("SELECT symbol FROM transactions WHERE user_id = ?", user_id):
        symbols.append(symbol["symbol"])

    if request.method == "POST":
        # Error handling form inputs
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Please select a symbol!")
        if not symbol in symbols:
            return apology("Invalid symbol!")

        shares = request.form.get("shares")
        if not shares:
            return apology("Please enter the number of shares!")

        shares = int(shares)
        if not shares > 0:
            return apology("Please enter a positive number greater than 0!")

        # User can't sell more shares than they own
        user_shares = db.execute("SELECT shares FROM transactions WHERE user_id = ? AND symbol = ?", user_id, symbol)[0]["shares"]
        if shares > user_shares:
            return apology(f"You have only {user_shares} shares of this stock!")

        # Check to see if number of shares will be 0 after transaction, if so delete the transaction, if not update it
        if user_shares == shares:
            db.execute("DELETE FROM transactions WHERE user_id = ? AND symbol = ?", user_id, symbol)
        else:
            db.execute("UPDATE transactions SET shares = ? WHERE user_id = ? AND symbol = ?", user_shares - shares, user_id, symbol)

        # Update users cash
        extra_cash = qoute["price"] * shares
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
        db.execute("UPDATE users SET cash = ? WHERE id = ?", (user_cash + extra_cash), user_id)

        # Add the transactions to the user's history
        qoute = lookup(symbol)
        db.execute("INSERT INTO histories (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)", user_id, symbol, (0 - shares), qoute["price"])

        return redirect("/")

    else:
        return render_template("sell.html", symbols=symbols)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
