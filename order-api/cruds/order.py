from models import Order
from schemas import OrderCreate
from sqlalchemy.orm import Session
import requests
from datetime import datetime
from jose import jwt,JWTError
import asyncio
import aiohttp

# SECRET_KEY = "3FIQodO54obEzChoXmZFaprULmWd1KkYqc5GbITvYwA="
# ALGORISM = "HS256"

class ProductNotFoundError(Exception):
    pass
class InsufficientStockError(Exception):
    pass
class ProductDiscontinuedError(Exception):
    pass


async def fetch_product(product_id :int):
    async with aiohttp.ClientSession() as session:
        async with session.get(
        f"http://localhost:8001/products/{product_id}"
        ) as response:
            if response.status != 200:
                raise ProductNotFoundError(f"商品ID:{product_id}の商品が見つかりません。")
            return await response.json()

async def ensure_product_exists(product_id :int):
    product =  await fetch_product(product_id)
    if product['status']==False:
        raise ProductDiscontinuedError(f"商品ID：{product_id}は販売中止です。")


async def fetch_stock(product_id :int):
    async with aiohttp.ClientSession() as session:
        async with session.get(
        f"http://localhost:8002/stock/{product_id}"
        ) as response:
            if response.status != 200:
                raise ProductNotFoundError(f"商品ID:{product_id}に在庫が見つかりません。")
            return await response.json()

async def ensure_stock_exists(product_id :int):
    stock = await fetch_stock(product_id)
    return stock['stock']

def confirm_stock(stock :int,quantity :int):
    if stock < quantity:
        raise InsufficientStockError(f"在庫が足りません（在庫：{stock}個、注文数：{quantity}個）")
        
    

async def ensure_stock_is_enough(product_id :int,quantity :int):
    stock = await ensure_stock_exists(product_id)
    confirm_stock(stock,quantity)
    return stock

async def update_stock(product_id :int,new_stock :int):
    async with aiohttp.ClientSession() as session:
        async with session.put(
            f"http://localhost:8002/stock/{product_id}",
            json={'stock':new_stock}
            ) as response:
            if response.status != 200:
                raise Exception(f"在庫を更新できません:status={response.status}")
    
async def update_product_status(product_id :int):
    async with aiohttp.ClientSession() as session:
        async with session.put(
            f"http://localhost:8001/products/{product_id}",
            json={'status':False}
            ) as response:
            if response.status != 200:
                raise Exception(f"販売状況を更新できません:status={response.status}")

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

async def notify_stock(product_id :int,stock :int,quantity :int):
    await update_stock(product_id,stock-quantity)

async def mark_as_unsellable(product_id :int):
    await update_product_status(product_id)

async def notify_product_status(product_id :int,stock :int,quantity :int):
    if stock - quantity ==0:
        await mark_as_unsellable(product_id)


OREDER_CONFIRMED_SUBSCRIBERS=[
    notify_stock,
    notify_product_status
]

async def publish_order_confirmed(product_id :int,stock :int,quantity :int):
    tasks=[
    handler(product_id,stock,quantity) for handler in OREDER_CONFIRMED_SUBSCRIBERS# 内包表記
    ]
    await asyncio.gather(*tasks)


async def order_confirm(db :Session,product_id :int,quantity :int,user_id :int):
    await ensure_product_exists(product_id)
    stock = await ensure_stock_is_enough(product_id,quantity)
    new_order = save_order(db,product_id,quantity,user_id)
    await publish_order_confirmed(product_id,stock,quantity)
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
    
    
    