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


@app.get("/book/<int:product_id>")
def product(product_id):
    books = get(f"{BACKEND_URL}/get_books").json()
    selected_product = None
    
    for product in books:
        if product['id'] == product_id:
            selected_product = product
            break

    if selected_product:
        return render_template("info.html", book=selected_product)
    else:
        return "Product not found", 404
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)