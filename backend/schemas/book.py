from pydantic import BaseModel, ConfigDict
from typing import Annotated, Union, Optional
from datetime import date
from fastapi import File, UploadFile

class BookData(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    #TODO id: int
    price: float
    title: str
    description: str
    author: str 
    #TODO release: Union[date| str]
    isbn: str
    photo: Optional[str]



