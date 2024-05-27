from main import app
from sqlalchemy import select
from datetime import datetime
from db import Session, Book
from schemas import BookData
from fastapi import UploadFile

def mock_data()->list[Book]:
    return [
        Book(title="МАТАН 1 клас",price=111.1, description="дуже важка книга", author="криса никоглайович", release=datetime.now(), isbn="17432384728736"),
        Book(title="Азбука 11 клас",price=99.9, description="не дуже важка книга", author="мій кіт", release=datetime.now(), isbn="1487148714871487"),
    ]


@app.get("/get_books")
def get_books():
    with Session.begin() as session:
        # session.add_all(mock_data())
        books = session.scalars(select(Book)).all()
        print("*"*80)
        print('\n' * 4)
        print(f'{[type(x.photo) for x in books]=}')
        books = [BookData.model_validate(book) for book in books]
        print('\n' * 4)
        print("*"*80)
        return books

@app.post("/create_book")
def create_book(data: BookData):
    with Session.begin() as session:
        book = Book(**data.model_dump())
        session.add(book)
        return book