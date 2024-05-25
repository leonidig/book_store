from .. import Base


from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date


class Book(Base):
    __tablename__ = "books"

    title: Mapped[str]
    price: Mapped[float]
    description: Mapped[str]
    author: Mapped[str]
    release: Mapped[date]
    isbn: Mapped[str] = mapped_column(String(13))
    # image_path: Mapped[str] = mapped_column(String(255), nullable=True)
