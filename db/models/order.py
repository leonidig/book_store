from .. import Base


from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date


class Order(Base):
    __tablename__ = "orders"

    nickname: Mapped[str]

    # status: Mapped[bool]

    country: Mapped[str]
    city: Mapped[str]
    street: Mapped[str]
    house: Mapped[str]