import os, json
from flask import Flask, session, redirect, render_template, request, jsonify, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required
from douban import *

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Use script env.sh to set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# By adding snippet update CSS
# https://stackoverflow.com/questions/21714653/flask-css-not-updating


@app.route("/")
@app.route("/book/")
#@login_required
def index():
    """ Show search box """

    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """ Log user in """

    # Forget any user_id
    session.clear()

    username = request.form.get("username")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("error.html", message="must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("error.html", message="must provide password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                            {"username": username})
        
        result = rows.fetchone()

        # Ensure username exists and password is correct
        if result == None or not check_password_hash(result[2], request.form.get("password")):
            return render_template("error.html", message="invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = result[0]
        session["user_name"] = result[1]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """ Log user out """

    # Forget any user ID
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """ Register user """
    
    # Forget any user_id
    session.clear()
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("error.html", message="must provide username")
        
        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("error.html", message="must provide password")

        # Ensure confirmation wass submitted 
        elif not request.form.get("confirmation"):
            return render_template("error.html", message="must confirm password")

        # Check passwords are equal
        elif not request.form.get("password") == request.form.get("confirmation"):
            return render_template("error.html", message="passwords didn't match")
        
        # Query database for username
        userCheck = db.execute("SELECT * FROM users WHERE username = :username",
                          {"username":request.form.get("username")}).fetchone()

        # Check if username already exist
        if userCheck:
            return render_template("error.html", message="username already exist")
        
        # Hash user's password to store in DB
        hashedPassword = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
        
        # Insert register into DB
        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
                            {"username":request.form.get("username"), 
                             "password":hashedPassword})

        # Commit changes to database
        db.commit()

        flash('Account created', 'info')

        # Redirect user to login page
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/search", methods=["GET"])
#@login_required
def search():
    """ Get books results """

    # Check if random select
    if request.args.get("lucky") == 'True':

        # Quickly select a random row from books table 
        rows = db.execute("SELECT isbn FROM books ORDER BY RANDOM() LIMIT 1;")

        # Fetch all the results
        book = rows.fetchall()

        # redirect to this page
        d = dict(book[0].items())
        return redirect("/book/"+d['isbn'])
    
    # Check book id was provided
    if not request.args.get("book"):
        return render_template("error.html", message="you must provide a book.")

    # Take input and add a wildcard
    query = "%" + request.args.get("book") + "%"

    # Capitalize all words of input for search
    query = query.title()

    begin = 0
    end = 20;

    # Customize search position
    if request.args.get("begin") and request.args.get("end"):
        begin = request.args.get("begin")
        end = request.args.get("end")
    
    rows = db.execute("(SELECT isbn, title, author, year FROM books WHERE \
                        isbn LIKE :query OR \
                        title LIKE :query OR \
                        author LIKE :query LIMIT :end) \
                        EXCEPT \
                        (SELECT isbn, title, author, year FROM books WHERE \
                        isbn LIKE :query OR \
                        title LIKE :query OR \
                        author LIKE :query LIMIT :begin)",
                        {"query": query,
                         "begin": begin,
                         "end": end})                   
    
    # Books not founded
    if rows.rowcount == 0:
        return render_template("error.html", message="we can't find books with that description.")
    
    # Fetch all the results
    books = rows.fetchall()

    booksPic = []
    
    # Assign pic
    for row in books:
        d = dict(row.items())
        pic = getBookBySearchSuggest(d['isbn'])
        if pic == None:
            pic = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAD0AAABYCAMAAABxhQ8yAAAAM1BMVEX///+ysrLb29v8/Pzr6+vp6en39/evr6/h4eHx8fHe3t6/v7/T09O7u7vMzMzk5OTGxsalfPg5AAABOklEQVRYhe2Xi26EIBBFcZwRWV7+/9cWi2sR8Mk21erRxcR4cgcMuDCk4yCjpj5K4+yaHaVGhje1n1G7l132vj9s+6nrjnqc+Y0jb0f9JqkdMkOXFJnYRlq3VKGY0teB2qxVbky6/HgYQx1XH2UTT2vWHsXEmm14NQcXWZuK7LLsT9vc8d0MeLvd1m/ZviaoJTvJltMvG8Iue6bfRXa12eYT9mYD/iA6vjPbBKPeyiHbbq+8igsvH/NK/IYtrIMsdss22AFypxhtAo+cf929rSAARxv9jdedbLps5WexuyW7XrFhcZZc126KbKUhtWmjDZPkvdkGcnaYDfq9jvIYCVk7zAZQnvjRDDl7O//BpvWHE2i0338nd/Hnu7lT7SwuYz+798d+7HPbx0EmBPYnIqH/Bc3QRpfxivgF4GQjuZBHoAAAAAAASUVORK5CYII='
        else:
            pic = pic['pic']
            # Sometimes picture is not available
            # douban image anti hotlink in https://ifttl.com/douban-img-anti-hotlink
        d['pic'] = pic
        booksPic.append(d)
    
    return render_template("results.html", books=booksPic, name=request.args.get("book"))

@app.route("/book/<isbn>", methods=['GET','POST'])
def book(isbn):
    """ Save user review and load same page with reviews updated."""

    # Post review here
    if request.method == "POST":

        # Already logged in
        try:
            currentUser = session["user_id"]
            
            # Fetch form data
            rating = request.form.get("rating")
            comment = request.form.get("comment")
            
            # Search book_id by ISBN
            row = db.execute("SELECT id FROM books WHERE isbn = :isbn",
                            {"isbn": isbn})

            # Save id into variable
            bookId = row.fetchone() # (id,)
            bookId = bookId[0]

            # Check for user submission (ONLY 1 review/user allowed per book)
            row2 = db.execute("SELECT * FROM reviews WHERE user_id = :user_id AND book_id = :book_id",
                        {"user_id": currentUser,
                         "book_id": bookId})

            # A review already exists
            if row2.rowcount == 1:
                
                flash('You already submitted a review for this book', 'warning')
                return redirect("/book/" + isbn)

            # Convert to save into DB
            if rating == "0":
                rating = None
            else:
                rating = int(rating)

            db.execute("INSERT INTO reviews (user_id, book_id, comment, rating, time) VALUES \
                        (:user_id, :book_id, :comment, :rating, NOW())",
                        {"user_id": currentUser, 
                        "book_id": bookId, 
                        "comment": comment, 
                        "rating": rating})

            # Commit transactions to DB and close the connection
            db.commit()

            flash('Review submitted!', 'info')
            return redirect("/book/" + isbn)
        
        # Didn't log in
        except KeyError:
            flash('You did not log in!')
            return redirect("/login?book=" + isbn)

    # Take the book ISBN and redirect to his page (GET)
    else:
        
        row = db.execute("SELECT id, isbn, title, author, year FROM books WHERE \
                        isbn = :isbn",
                        {"isbn": isbn})

        bookInfo = row.fetchall()

        # Check if the user have submission
        commented = False
        uid = None
        try:
            currentUser = session["user_id"]
            uid = currentUser
            row2 = db.execute("SELECT * FROM reviews WHERE user_id = :user_id AND book_id = :book_id",
                          {"user_id": currentUser,
                           "book_id": int(bookInfo[0]['id'])
                           })
            # The review already exists
            if row2.rowcount == 1:
                commented = True
        except KeyError:
            pass

        """ Douban info """

        # Get book info from book.douban.com
        # Disabled because of invalid API source
        # bookInfo.append({'douban':getBookBySearch(isbn)})

        """ Users reviews """

         # Search book_id by ISBN
        row = db.execute("SELECT id FROM books WHERE isbn = :isbn",
                        {"isbn": isbn})

        # Save id into variable
        book = row.fetchone() # (id,)
        book = book[0]

        # Fetch book reviews
        results = db.execute("SELECT users.username, comment, rating, user_id,\
                            to_char(time, 'DD Mon YY ') as time \
                            FROM users \
                            INNER JOIN reviews \
                            ON users.id = reviews.user_id \
                            WHERE book_id = :book \
                            ORDER BY time",
                            {"book": book})

        reviews = results.fetchall()

        return render_template("book.html", bookInfo=bookInfo, reviews=reviews, commented=commented, uid=uid)

@app.route("/api/")
@app.route("/api/<isbn>", methods=['GET'])
@login_required
def api_call(isbn=''):
    if isbn:
        row = db.execute("SELECT title, author, year, isbn, \
                        COUNT(reviews.id) as review_count, \
                        AVG(reviews.rating) as average_score \
                        FROM books \
                        LEFT JOIN reviews \
                        ON books.id = reviews.book_id \
                        WHERE isbn = :isbn \
                        GROUP BY title, author, year, isbn",
                        {"isbn": isbn})

        # Error checking
        if row.rowcount != 1:
            print(row.rowcount)
            return jsonify({"message": "Invalid book ISBN"}), 422

        # Fetch result from RowProxy    
        tmp = row.fetchone()

        # Convert to dict
        result = dict(tmp.items())

        # Add successful message
        result['message'] = 'successful'
        
        # calculate average score
        if result['review_count'] == 0:
            pass
        else:
            result['average_score'] = float('%.2f'%(result['average_score']))
        return jsonify(result)
    else:
        return render_template("api.html")
