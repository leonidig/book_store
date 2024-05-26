from main import app
from sqlalchemy import select
from datetime import datetime
from db import Session, Book
from schemas import BookData

def mock_data()->list[Book]:
    return [
        Book(title="МАТАН 1 клас",price=111.1, description="дуже важка книга", author="криса никоглайович", release=datetime.now(), isbn="17432384728736"),
        Book(title="Азбука 11 клас",price=99.9, description="не дуже важка книга", author="мій кіт", release=datetime.now(), isbn="1487148714871487"),
    ]


@app.get("/get_books")
def get_books():
    with Session.begin() as session:
        session.add_all(mock_data())
        books = session.scalars(select(Book)).all()
        books = [BookData.model_validate(book) for book in books]
        print(f'{"*"*80}"\n"{books=}')
        return books