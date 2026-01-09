from fastapi import FastAPI,Depends,APIRouter
import requests
from fastapi.security import OAuth2PasswordRequestForm,APIKeyHeader
from typing import Annotated,Optional
from pydantic import BaseModel,Field
from schemas import CreateUser,ItemCreate,ItemUpdate,StockCreate,StockUpdate

app = FastAPI()
FormDependency = Annotated[OAuth2PasswordRequestForm,Depends()]
api_key_header = APIKeyHeader(name="Authorization")

# ====================
# product-api
# ====================
@app.get("/products", tags=['products'])
def get_products():
    response = requests.get(
        f"https://product-api-987336615042.asia-northeast1.run.app/products"
    )
    return response.json()

@app.post("/products",tags=['products'])
def create_product(create_item :ItemCreate):
    response = requests.post(
        f"https://product-api-987336615042.asia-northeast1.run.app/products",
        json=create_item.model_dump()
    )
    return response.json()

@app.put("/products/{id}",tags=['products'])
def update_product(id :int,update_item :ItemUpdate):
    response = requests.put(
        f"https://product-api-987336615042.asia-northeast1.run.app/products/{id}",
        json=update_item.model_dump()    
    )
    return response.json()

# ====================
# stock-api
# ====================
@app.get("/stock",tags=['stock'])
def get_stock():
    response = requests.get(
        f"https://stock-api-987336615042.asia-northeast1.run.app/stock"
    )
    return response.json()

@app.post("/stock",tags=['stock'])
def create_stock(create_stock :StockCreate):
    response = requests.post(
        f"https://stock-api-987336615042.asia-northeast1.run.app/stock",
        json=create_stock.model_dump()
    )
    return response.json()

@app.put("/stock",tags=['stock'])
def update_stock(id :int,update_stock :StockUpdate):
    response = requests.put(
        f"https://stock-api-987336615042.asia-northeast1.run.app/stock{id}",
        json=update_stock.model_dump()
    )
    return response.json()

# ====================
# auth-api
# ====================
@app.post("/login",tags=['auth'])
def login(form_data:FormDependency):
    """ログインリクエストをauth-apiに中継する
    
    フォームからユーザー名とパスワードを取得して、
    auth-apiにログイン処理を委譲する
    JWTの発行はauth-api側で行われる
    """
    username=form_data.username
    password=form_data.password
    response = requests.post(
        f"https://auth-api-987336615042.asia-northeast1.run.app/auth/login",
        data={'username':username,'password':password}
    )
    return response.json()

@app.post("/signup",tags=['auth'])
def signup(user_create :CreateUser):
    """ユーザー作成リクエストをauth-apiに中継する

    リクエストボディからユーザー情報を取得して、
    auth-apiにユーザー作成処理を委譲する
    
    """
    response = requests.post(
        f"https://auth-api-987336615042.asia-northeast1.run.app/auth/signup",
        json=user_create.model_dump()
    )
    return response.json()

# ====================
# order-api
# ====================
@app.post("/order",tags=['order'])
def order(product_id:int,quantity:int,authorization: str = Depends(api_key_header)):
    """注文APIへのリクエストを中継する

    注文確定処理を order-api に委譲する
    注文確定後に発行されるイベントを契機として、
    在庫更新や販売状況更新は各サービス側で行われる

    Gatewayでは処理は行わない

    """
    response = requests.post(
        f"https://order-api-987336615042.asia-northeast1.run.app/order?product_id={product_id}&quantity={quantity}",
        headers={'Authorization':authorization}
    )
    return response.json()