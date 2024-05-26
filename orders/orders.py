from fastapi import FastAPI
from sqlalchemy import select
from pydantic import BaseModel
import sys, os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db import Session, User, Book, Order

app = FastAPI()

class Data(BaseModel):
    nickname: str
    country: str
    city: str
    street: str
    house: str
    
#nickname: str, country: str, city: str, street: str, house: str    
@app.post("/basket/add")
def post_order(data: Data):
    
    with Session.begin() as session:
        order = Order(nickname=data.nickname, country=data.country , city=data.city, street=data.street, house=data.house)
        session.add(order)
        return order 