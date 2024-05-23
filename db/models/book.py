from .. import Base

from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped, mapped_column
from datetime import date


class Book(Base):
    __tablename__ = "books"

    title: Mapped[str]
    autor: Mapped[str]
    release: Mapped[date]
    description: Mapped[str]