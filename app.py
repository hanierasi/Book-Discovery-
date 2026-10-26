from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from database import add_user
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


if __name__ == "__main__":
    app.run(debug=True)
