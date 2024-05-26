from pydantic import BaseModel, ConfigDict
from datetime import date

class BookData(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    price: float
    title: str
    description: str
    author: str
    release: date
    isbn: str



