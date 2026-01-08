from models import Order
from sqlalchemy.orm import Session
from datetime import datetime
import aiohttp
import redis
import json

redis_client = redis.Redis(host='localhost',port=6379,decode_responses=True)

class ProductNotFoundError(Exception):
    pass
class InsufficientStockError(Exception):
    pass
class ProductDiscontinuedError(Exception):
    pass


async def fetch_product(product_id :int) -> dict:
    """商品情報をproduct-apiから取得する

    指定された商品IDの情報を外部のAPIから取得する
    商品IDが存在しない場合はエラーをだす

    Args:
        product_id: 商品ID

    Returns:
        商品情報（JSON）

    Raises:
        ProductNotFoundError: 商品が存在しない場合

    """
    async with aiohttp.ClientSession() as session:
        async with session.get(
        f"http://localhost:8001/products/{product_id}"
        ) as response:
            if response.status != 200:
                raise ProductNotFoundError(f"商品ID:{product_id}の商品が見つかりません。")
            return await response.json()

async def ensure_product_exists(product_id :int):
    """販売中であることを保証する

    指定された商品IDが販売中であることを確認する
    販売中止の場合はエラーをだす

    Args:
        product_id: 商品ID
    
    Raises:
        ProductNotFoundError: 商品が存在しない場合
    """
    product =  await fetch_product(product_id)
    if product['status']==False:
        raise ProductDiscontinuedError(f"商品ID：{product_id}は販売中止です。")


async def fetch_stock(product_id :int):
    """在庫情報をstock-apiから取得する

    指定された商品IDの情報を外部APIから取得する
    商品IDが存在しない場合はエラーをだす
    
    Args:
        product_id: 商品ID

    Returns:
        在庫情報（JSON）

    Raises:
        ProductNotFoundError: 商品が存在しない場合
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(
        f"http://localhost:8002/stock/{product_id}"
        ) as response:
            if response.status != 200:
                raise ProductNotFoundError(f"商品ID:{product_id}に在庫が見つかりません。")
            return await response.json()

async def ensure_stock_exists(product_id :int):
    """在庫数が存在することを確認し、在庫数を返す

    指定された商品IDの在庫を取得する
    在庫がない場合はエラーを返す

    Args:
        product_id: 商品ID

    Returns:
        stock: 在庫数
    
    Raises:
        ProductNotFoundError: 商品が存在しない場合
    
    """
    stock = await fetch_stock(product_id)
    return stock['stock']

def confirm_stock(stock :int,quantity :int):
    """在庫数が注文数以上であることを保証する

    Args:
        stock: 在庫数
        quantity: 注文数

    Raises:
        InsufficientStockError: 在庫が不足している場合
    
    """
    if stock < quantity:
        raise InsufficientStockError(f"在庫が足りません（在庫：{stock}個、注文数：{quantity}個）")
        
    

async def ensure_stock_is_enough(product_id :int,quantity :int):
    stock = await ensure_stock_exists(product_id)
    confirm_stock(stock,quantity)
    return stock

def create_order_entity(product_id :int,quantity :int,user_id :int):
    """注文エンティティを生成する

    DBには保存せず、Orderオブジェクトのみを生成する。

    Args:
        product_id: 商品ID
        quantity: 注文数
        user_id: ユーザーID

    Returns:
        new_order: 注文エンティティ
    """
    new_order = Order(
        # **order_create.model_dump()
        product_id = product_id,
        quantity = quantity,
        order_at = datetime.now(),
        user_id = user_id
        )
    return new_order

def save_order(db :Session,product_id :int,quantity :int,user_id :int):
    """注文情報を保存する

    注文エンティティをデータベースに保存する

    Args:
        product_id: 商品ID
        quantity: 注文数
        user_id: ユーザーID

    Returns:
        Order: 作成された注文情報
    
    """
    new_order = create_order_entity(product_id,quantity,user_id)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

def publish_order_confirmed(product_id :int,stock :int,quantity :int):
    """注文確定イベントを発行する

    注文が確定したことを通知するために
    商品ID、在庫数、注文数を含むイベントをRedisにPublishする
    在庫数更新など後続処理は別のサービスに委ねる

     Args:
        product_id: 商品ID
        stock: 在庫数
        quantity: 注文数
        

    """
    event_data={
        'product_id':product_id,
        'stock':stock,
        'quantity':quantity
    }
    redis_client.publish("order_confirmed",json.dumps(event_data))# イベント発行
    print(f'publish event:{event_data}')


async def order_confirm(db :Session,product_id :int,quantity :int,user_id :int) -> dict:
    """注文処理
    
    販売状況と在庫を確認し、注文データを保存、イベントを発行

    Args:
        db: データベースセッション
        product_id: 商品ID
        quantity: 注文数
        user_id: ログインしているユーザーのID
        
    Returns:
        new_order: 作成された注文情報
        
    Raises:
        ProductNotFoundError: 商品が存在しない場合
        ProductDiscontinuedError: 商品が販売中止の場合
        InsufficientStockError: 在庫が不足している場合

    """
    await ensure_product_exists(product_id) # 販売中か確認
    stock = await ensure_stock_is_enough(product_id,quantity) # 在庫の確認と、在庫返却
    new_order = save_order(db,product_id,quantity,user_id) # 注文保存
    publish_order_confirmed(product_id,stock,quantity) # イベント発行
    return new_order


