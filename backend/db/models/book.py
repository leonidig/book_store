from .. import Base
from sqlalchemy import String, Column
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date
from sqlalchemy.dialects.sqlite import BLOB

class Book(Base):
    __tablename__ = "books"

    title: Mapped[str]
    price: Mapped[float]
    description: Mapped[str]
    author: Mapped[str]
    release: Mapped[date] = mapped_column(nullable=True)
    isbn: Mapped[str] = mapped_column(String(13))
    photo: Mapped[str] = mapped_column(nullable=True)
