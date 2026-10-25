from flask import Flask, render_template ,request
import requests

app=Flask(__name__)

@app.route("/")
def home():
    query=request.args.get("query","")
    books =[]

    if query :
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

    return render_template(
        "book_detail.html",
        book=book
    )

if __name__ == "__main__":
    app.run(debug=True)