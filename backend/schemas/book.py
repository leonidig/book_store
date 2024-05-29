from pydantic import BaseModel, ConfigDict
from typing import Annotated, Union, Optional
from datetime import date
from fastapi import File, UploadFile

class BookData(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    price: float
    title: str
    description: str
    book_creator: str
    author: str 
    isbn: str
    photo: Optional[str]


class DeletedBook(BaseModel):
    book_id: int
    current_user: str
    book_creator: str
