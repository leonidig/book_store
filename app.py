from os import getenv

from flask import Flask, render_template, request, redirect, flash, url_for
from requests import get, Response, post
from flask_login import current_user, login_required, LoginManager
from forms import RegisterForm, LoginForm
from sqlalchemy import select
from db import User, Session
from flask_login import login_user
from dotenv import load_dotenv


load_dotenv()
SECRET_KEY = getenv("SECRET_KEY")
app = Flask("frontend")
app.config['SECRET_KEY'] = SECRET_KEY
BOOKS_URL = "http://127.0.0.1:8000"
ORDERS_URL = "http://127.0.0.1:5050"
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)



@app.get("/")
def index():
    books = {
        "books":get(f"{BOOKS_URL}/get_books").json()
    }
    print(books)
    return render_template("index.html", **books)

                                                       
@app.get("/book/<int:product_id>")
@login_required
def product(product_id):                    
    books = get(f"{BOOKS_URL}/get_books").json()
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
    books = get(f"{BOOKS_URL}/get_books").json()
    
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
    order = post(f"{ORDERS_URL}/basket/add", json=data)
    if order.status_code == 200:
        response_data = order.json()
        return(response_data)
    
    return(f"Error {order.status_code}")
    
    

if __name__ == '__main__':
    app.run(debug=True, port=5000)