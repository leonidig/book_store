from main import app
from db import Session, Order
from schemas import OrderData

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