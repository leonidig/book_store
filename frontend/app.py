from os import getenv
import os, sys
from flask import Flask, render_template, request, redirect, flash, url_for
from requests import get, Response, post
from flask_login import current_user, login_required, LoginManager
from forms import RegisterForm, LoginForm
from sqlalchemy import select
from werkzeug.utils import secure_filename
from flask_login import login_user
from dotenv import load_dotenv
from db import Session, User
from os import getenv
from base64 import b64encode


load_dotenv()
SECRET_KEY = getenv("SECRET_KEY")
app = Flask("frontend")
app.config['SECRET_KEY'] = SECRET_KEY
BACKEND_URL = getenv("BACKEND_URL")#"http://127.0.0.1:8000"

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

import logging

@app.get("/")
def index():
    books = {
        "books":get(f"{BACKEND_URL}/get_books").json()
    }
    print(books)
    return render_template("index.html", **books)

@app.get("/search")
def search():
    query = request.args.get('query','')
    if query:
        books = get(f"{BACKEND_URL}/get_books").json()
        filtered = [book for book in books if query.lower() in book['title'].lower()]
        return render_template("index.html", books = filtered, query = query)
    


                                                       
@app.get("/book/<int:product_id>")
@login_required
def product(product_id):                    
    books = get(f"{BACKEND_URL}/get_books").json()
    selected_product = None
    
    for product in books:
        if product['id'] == product_id:
            selected_product = product
            break

    if selected_product:
        return render_template("info.html", book=selected_product, product_id=product_id)
    else:
        return "Product not found", 404

@login_manager.user_loader
def load_user(user_id):
    with Session.begin() as session:
        user = session.scalar(select(User).where(User.id == user_id))
        if user:
            user = User(email=user.email)
            return user
    

@app.get('/register')
def register():
    form = RegisterForm()
    return render_template('form_template.html', form=form)

@app.post('/register')
def register_post():
    form = RegisterForm()
    if form.validate_on_submit():
       with Session.begin() as session:
           user = session.scalar(select(User).where(User.email == form.email.data))
           if user:
               flash("User exists!")
               return redirect(url_for('register'))
           pwd = form.password.data
           user = User(
               nickname = form.email.data.split('@')[0],
               email = form.email.data,
               password = pwd,
           )
           session.add(user)
       return redirect(url_for('login'))
    return render_template('form_template.html', form=form)

@app.get('/login')
def login():
    form = LoginForm()
    return render_template('form_template.html', form=form)

@app.post('/login')
def login_post():
    form = LoginForm()
    if form.validate_on_submit():
        with Session.begin() as session:
            user = session.query(User).where(User.nickname == form.nickname.data).first()
            if user:
                if user.password == form.password.data:
                    login_user(user)
                    return redirect(url_for("index"))
                flash("Wrong password")
            else:
                flash("Wrong nickname")
    return render_template('form_template.html', form=form)


@app.get("/basket/<int:product_id>")
def basket(product_id):
    selected_product = None
    books = get(f"{BACKEND_URL}/get_books").json()
    
    for product in books:
        if product['id'] == product_id:
            selected_product = product
            break

    if selected_product is None:
        return "Product not found", 404
    
    return render_template('basket.html', book=selected_product, product_id=product_id)


@app.post("/basket/<int:product_id>")
def post_basket(product_id):
    data = {
        "nickname": current_user.email,
        "country": request.form['country'],
        "city": request.form['city'],
        "street": request.form['street'],
        "house": request.form['house']
    }
    print(data)
    order = post(f"{BACKEND_URL}/basket/add", json=data)
    if order.status_code == 200:
        response_data = order.json()
        return redirect(url_for('index'))

    
    return(f"Error {order.status_code}")
    
@app.post("/create_book")
def create_book():
    file = request.files.get('photo')
    filename = secure_filename(file.filename)
    file.save(filename)
    with open(filename, "rb") as filename:
        photo = filename.read()
    # price: float
    # title: str
    # description: str
    # author: str
    # isbn: str
    data = {
        # TODO: "id"
        "title": request.form['title'],
        "description": request.form['description'],
        "author": request.form['author'],
        "price": float(request.form['price']),
        # TODO:"release": 
        "isbn": request.form['isbn'],
        "photo": b64encode(photo).decode("utf-8"),
    }
    
    # return data
    book = post(f"{BACKEND_URL}/create_book", json=data)
    if book.status_code == 200:
        return redirect(url_for("index"))
    return(f"Error {book.status_code}")

 
 
@app.get('/create_book')
def get_create_book():
    return render_template("create.html")


if __name__ == '__main__':
    app.run(debug=True, port=5000)