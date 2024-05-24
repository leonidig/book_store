from fastapi import FastAPI
from db import Book, Session
from sqlalchemy import select
from datetime import datetime
import random

app = FastAPI()



@app.get("/get_books")
def get_books():
    with Session.begin() as session:
        book = Book(title="mock", description="mock mock", author="mock author", release=datetime.now(), isbn="2235678903945828")
        session.add(book)
        books = session.scalars(select(Book)).all()
        
        return [{"id":book.id, "title": book.title, "description": book.description, "author": book.author, "release": book.release, "isbn": book.isbn}for book in books]