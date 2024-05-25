from fastapi import FastAPI
from db import Order
from sqlalchemy import select
from db import Session
from pydantic import BaseModel

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