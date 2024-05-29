from main import app
from db import Session, Order
from schemas import OrderData, OrderDelete
from sqlalchemy import select

# def mock_data()->list[Book]: #TODO: Переробити мок данних для замовлень
#     return [
#         Book(title="МАТАН 1 клас",price=111.1, description="дуже важка книга", author="криса никоглайович", release=datetime.now(), isbn="17432384728736"),
#         Book(title="Азбука 11 клас",price=99.9, description="не дуже важка книга", author="мій кіт", release=datetime.now(), isbn="1487148714871487"),
#     ]


@app.post("/basket/add")
def post_order(data: OrderData):
    
    with Session.begin() as session:
        
        order = Order(**data.model_dump())
        session.add(order)
        return order 

@app.get("/orders/{user_email}")
def user_orders(user_email):
    with Session.begin() as session:
        orders = session.scalars(select(Order).where(Order.nickname == user_email)).all()
        print(orders)
        return [order.book_name for order in orders]
    
@app.delete("/cancel_order")
def cancel_order(data: OrderDelete):
    with Session.begin() as session:
        order = session.scalar(select(Order).where(Order.book_name == data.book_name).where(Order.nickname == data.current_user))
        session.delete(order)
        return "Book succesfully deleted"
    