from models import Order
from schemas import OrderCreate
from sqlalchemy.orm import Session
import requests
from datetime import datetime
from jose import jwt,JWTError

SECRET_KEY = "3FIQodO54obEzChoXmZFaprULmWd1KkYqc5GbITvYwA="
ALGORISM = "HS256"

class ProductNotFoundError(Exception):
    pass
class InsufficientStockError(Exception):
    pass


def fetch_product(product_id :int):
    response_product = requests.get(
        f"http://localhost:8001/products/{product_id}"
    )
    if response_product.status_code != 200:
        raise ProductNotFoundError(f"商品ID:{product_id}が見つかりません。")
    return response_product.json()

def ensure_product_exists(product_id :int):
    product = fetch_product(product_id)
    return product['id']


def fetch_stock(product_id :int):
    response_stock = requests.get(
        f"http://localhost:8002/stock/{product_id}"
    )
    print(f'Response Body: {response_stock.json()["stock"]}')
    return response_stock.json()

def ensure_stock_exists(product_id):
    stock = fetch_stock(product_id)
    return stock['stock']

def confirm_stock(stock :int,quantity :int):
    if stock < quantity:
        raise InsufficientStockError(f"在庫が足りません（在庫：{stock}個、注文数：{quantity}個）")
    

def ensure_stock_is_enough(product_id :int,quantity :int):
    stock =ensure_stock_exists(product_id)
    confirm_stock(stock,quantity)
    return stock

def update_stock(product_id :int,new_stock :int):
    response = requests.put(
            f"http://localhost:8002/stock/{product_id}",
            json={'stock':new_stock}
        )
    
def update_product_status(product_id :int):
    response = requests.put(
            f"http://localhost:8001/products/{product_id}",
            json={'status':False}
    )
    
def create_order_entity(product_id :int,quantity :int,user_id :int):
    new_order = Order(
        # **order_create.model_dump()
        product_id = product_id,
        quantity = quantity,
        order_at = datetime.now(),
        user_id = user_id
        )
    return new_order

def save_order(db :Session,product_id :int,quantity :int,user_id :int):
    new_order = create_order_entity(product_id,quantity,user_id)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

def notify_stock(product_id :int,stock :int,quantity :int):
    update_stock(product_id,stock-quantity)

def mark_as_unsellable(product_id :int):
    update_product_status(product_id)

def notify_product_status(product_id :int,stock :int,quantity :int):
    if stock - quantity ==0:
        mark_as_unsellable(product_id)


OREDER_CONFIRMED_SUBSCRIBERS=[
    notify_stock,
    notify_product_status
]

def publish_order_confirmed(product_id :int,stock :int,quantity :int):
    for handler in OREDER_CONFIRMED_SUBSCRIBERS:
        handler(product_id,stock,quantity)



def order_confirm(db :Session,product_id :int,quantity :int,user_id :int):
    product_id =ensure_product_exists(product_id)
    stock = ensure_stock_is_enough(product_id,quantity)
    new_order = save_order(db,product_id,quantity,user_id)
    publish_order_confirmed(product_id,stock,quantity)
    return new_order
    

# def create_order(db :Session,product_id :int,quantity :int,user_id :int):
    
#     # 商品情報取得
#     response_product = requests.get(
#         f"http://localhost:8001/products/{product_id}"
#     )
#     if response_product.status_code != 200:
#         raise ProductNotFoundError(f"商品ID:{product_id}が見つかりません。")
    
#     print(f"Response Body: {response_product.text}")
#     product = response_product.json()
#     # 在庫があるかを確認
#     response_stock = requests.get(
#         f"http://localhost:8002/stock/{product_id}"
#     )
#     print(f'Response Body: {response_stock.json()["stock"]}')
#     stock = response_stock.json()["stock"]

    
#     if stock >= quantity:
#         # 在庫を減らす
#         response = requests.put(
#             f"http://localhost:8002/stock/{product_id}",
#             json={'stock':stock - quantity}
#         )
#         new_order = Order(
#         # **order_create.model_dump()
#         product_id = product_id,
#         quantity = quantity,
#         order_at = datetime.now(),
#         user_id = user_id
#         )
#         db.add(new_order)
#         db.commit()
#         db.refresh(new_order)
#         print(f"New Order ID: {new_order.id}")
#         print(f"Product ID: {new_order.product_id}")
#         print(f"Quantity: {new_order.quantity}")
#         print(f"order_at: {new_order.order_at}")
#         print(f"user_id: {new_order.user_id}")
#         return new_order
#     else:
#         raise InsufficientStockError(f"在庫が足りません（在庫：{stock}個、注文数：{quantity}個）")
    
    
    