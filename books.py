from fastapi import FastAPI
from db import Book, Session
from sqlalchemy import select
from datetime import datetime
import random


app = FastAPI()


def mock_data()->list[Book]:
    return [
        Book(title="МАТАН 1 клас",price=111.1, description="дуже важка книга", author="криса никоглайович", release=datetime.now(), isbn="17432384728736"),
        Book(title="Азбука 11 клас",price=99.9, description="не дуже важка книга", author="мій кіт", release=datetime.now(), isbn="1487148714871487"),
    ]

@app.get("/get_books")
def get_books():
    with Session.begin() as session:
        # book1 = 
        # book2 = Book(title="Азбука 11 клас",price=99.9, description="не дуже важка книга", author="мій кіт", release=datetime.now(), isbn="1487148714871487")
        # session.add(book1)
        # session.add(book2)
        session.add_all(mock_data())
        books = session.scalars(select(Book)).all()
        
        return [{"id":book.id, "price": book.price, "title": book.title, "description": book.description, "author": book.author, "release": book.release, "isbn": book.isbn}for book in books]