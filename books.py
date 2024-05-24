from fastapi import FastAPI
from db import Book, Session
from sqlalchemy import select
from datetime import datetime
import random

app = FastAPI()



@app.get("/get_books")
def get_books():
    with Session.begin() as session:
        book1 = Book(title="МАТАН 1 клас", description="дуже важка книга", author="криса никоглайович", release=datetime.now(), isbn="1743ге2384728736")
        book2 = Book(title="Азбука 11 клас", description="не дуже важка книга", author="мій кіт", release=datetime.now(), isbn="1487148714871487")
        session.add(book1)
        session.add(book2)

        books = session.scalars(select(Book)).all()
        
        return [{"id":book.id, "title": book.title, "description": book.description, "author": book.author, "release": book.release, "isbn": book.isbn}for book in books]