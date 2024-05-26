from pydantic import BaseModel


class OrderData(BaseModel):
    nickname: str
    country: str
    city: str
    street: str
    house: str