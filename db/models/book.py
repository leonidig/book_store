from .. import Base


from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date


class Book(Base):
    __tablename__ = "books"

    title: Mapped[str]
    description: Mapped[str]
    author: Mapped[str]
    release: Mapped[date]
    isbn: Mapped[str] = mapped_column(String(13))