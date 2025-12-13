from models import Order
from schemas import OrderCreate
from sqlalchemy.orm import Session
import requests
from datetime import datetime

class ProductNotFoundError(Exception):
    pass
class InsufficientStockError(Exception):
    pass

def create_order(db :Session,product_id :int,quantity :int):


    response_product = requests.get(
        f"http://localhost:8001/products/{product_id}"
    )
    if response_product.status_code != 200:
        raise ProductNotFoundError(f"商品ID:{product_id}が見つかりません。")
    
    print(f"Response Body: {response_product.text}")
    product = response_product.json()

    response_stock = requests.get(
        f"http://localhost:8002/stock/{product_id}"
    )
    print(f'Response Body: {response_stock.json()["stock"]}')
    stock = response_stock.json()["stock"]

    if stock >= quantity:
        response = requests.put(
            f"http://localhost:8002/stock/{product_id}",
            json={'stock':stock - quantity}
        )
        new_order = Order(
        # **order_create.model_dump()
        product_id = product_id,
        quantity = quantity,
        order_at = datetime.now()
        )
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        print(f"New Order ID: {new_order.id}")
        print(f"Product ID: {new_order.product_id}")
        print(f"Quantity: {new_order.quantity}")
        print(f"Quantity: {new_order.order_at}")
        return new_order
    else:
        raise InsufficientStockError(f"在庫が足りません（在庫：{stock}個、注文数：{quantity}個）")
    
    
    