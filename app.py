from flask import Flask, render_template, request, redirect, url_for, flash , session
import sqlite3
from database import add_user , verify_user,save_book,get_user_books
import requests

app = Flask(__name__)
app.secret_key = "dev-only-change-this-to-a-random-secret"


@app.route("/")
def home():
    query = request.args.get("query", "")
    books = []

    if query:
        url = "https://openlibrary.org/search.json"
        params = {
            "q": query,
            "fields": "key,title,author_name,first_publish_year,cover_i",
            "limit": 12
        }

        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        books = data.get("docs", [])

    return render_template(
        "index.html",
        query=query,
        books=books
    )


@app.route("/book/<path:book_key>")
def book(book_key):
    url = f"https://openlibrary.org/{book_key}.json"
    response = requests.get(url, timeout=10)
    book = response.json()

    return render_template("book_detail.html", book=book)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Username and password are required.", "error")
            return redirect(url_for("register"))

        try:
            add_user(username, password)
            flash("Registration successful!", "success")
            return redirect(url_for("home"))

        except sqlite3.IntegrityError:
            flash("This username is already taken.", "error")
            return redirect(url_for("register"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user_id = verify_user(username, password)

        if user_id:
            session["user_id"] = user_id
            session["username"] = username

            flash("Login successful!", "success")
            return redirect(url_for("home"))

        flash("Invalid username or password.", "error")
        return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logout successful!", "success")
    return redirect(url_for("home"))

@app.route("/save-book/<path:book_key>", methods=["POST"])
def save_book_route(book_key):
    if not session.get("user_id"):
        flash("Please sign in to save books.", "error")
        return redirect(url_for("login"))

    user_id = session["user_id"]

    save_book(user_id, book_key)

    flash("Book saved or already in your library.", "success")

    return redirect(url_for("home", query=request.form.get("query", "")))

@app.route("/my-library")
def my_library():
    if not session.get("user_id"):
        flash("Please sign in to view your library.", "error")
        return redirect(url_for("login"))

    user_id = session["user_id"]

    books = get_user_books(user_id)

    return render_template("my_library.html", books=books)

if __name__ == "__main__":
    app.run(debug=True)
