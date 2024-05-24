from flask import Flask, render_template, request
from requests import get, Response

app = Flask("frontend")
BACKEND_URL = "http://127.0.0.1:8000"


@app.get("/")
def index():
    books = {
        "books":get(f"{BACKEND_URL}/get_books").json()
    }
    print(books)
    return render_template("index.html", **books)


if __name__ == '__main__':
    app.run(debug=True, port=5000)