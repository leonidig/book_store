from .. import Base
from sqlalchemy.orm import Mapped


class Order(Base):
    __tablename__ = "orders"
    
    nickname: Mapped[str]
    # status: Mapped[bool]
    country: Mapped[str]
    city: Mapped[str]
    street: Mapped[str]
    house: Mapped[str]
    book_name: Mapped[str]