from pydantic import BaseModel


class OrderData(BaseModel):
    nickname: str
    country: str
    city: str
    street: str
    house: str
    book_name: str
    
class OrderDelete(BaseModel):
    book_name: str
    current_user: str