from fastapi import FastAPI,Depends,APIRouter,HTTPException
import requests
from fastapi.security import OAuth2PasswordRequestForm,APIKeyHeader
from typing import Annotated,Optional
from pydantic import BaseModel,Field
from schemas import CreateUser,ItemCreate,ItemUpdate,StockCreate,StockUpdate
from requests.exceptions import RequestException

app = FastAPI()
FormDependency = Annotated[OAuth2PasswordRequestForm,Depends()]
api_key_header = APIKeyHeader(name="Authorization")

# 共通エラー関数
def raise_if_error_response(response,service_name:str):
    if response.status_code >=400:
        try:
            detail=response.json().get('detail','不明なエラー')
        except ValueError:
            detail='不明エラー'
        raise HTTPException(
            status_code=response.status_code,
            detail={
                "service":service_name,
                "message":detail}
        )
def handle_requesterror(service_name:str):
    raise HTTPException(status_code=503,detail=f"{service_name}に接続できません")



# ====================
# product-api
# ====================
@app.get("/products", tags=['products'])
def get_products():
    try:
        response = requests.get(
            "http://localhost:8001/products"
        )
        
    except RequestException:
        handle_requesterror('product_api')
    raise_if_error_response(response,'product_api')

    return response.json()



@app.post("/products",tags=['products'])
def create_product(create_item :ItemCreate):
    try:
        response = requests.post(
            "http://localhost:8001/products",
            json=create_item.model_dump()
        )
    except RequestException:
        handle_requesterror('product_api')
    raise_if_error_response(response,'product-api')
    return response.json()

@app.put("/products/{id}",tags=['products'])
def update_product(id :int,update_item :ItemUpdate):
    try:
        response = requests.put(
        f"http://localhost:8001/products/{id}",
        json=update_item.model_dump()    
    )
    except RequestException:
        handle_requesterror('product-api')
    raise_if_error_response(response,'product-api')
    return response.json()

# ====================
# stock-api
# ====================
@app.get("/stock",tags=['stock'])
def get_stock():
    try:
        response = requests.get(
            "http://localhost:8002/stock"
        )
    except RequestException:
        handle_requesterror('stock-api')
    raise_if_error_response(response,'stock-api')
    return response.json()

@app.post("/stock",tags=['stock'])
def create_stock(create_stock :StockCreate):
    try:
        response = requests.post(
        "http://localhost:8002/stock",
        json=create_stock.model_dump()
    )
    except RequestException:
        handle_requesterror('stock-api')
    raise_if_error_response(response,'stock-api')
    return response.json()

@app.put("/stock",tags=['stock'])
def update_stock(id :int,update_stock :StockUpdate):
    try:
        response = requests.put(
        f"http://localhost:8002/stock/{id}",
        json=update_stock.model_dump()
    )
    except RequestException:
        handle_requesterror('stock-api')
    raise_if_error_response(response,'stock-api')
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
    try:
        response = requests.post(
        "http://localhost:8004/auth/login",
        data={'username':username,'password':password}
    )
    except RequestException:
        handle_requesterror('auth-api')
    raise_if_error_response(response,'auth-api')
    return response.json()

@app.post("/signup",tags=['auth'])
def signup(user_create :CreateUser):
    """ユーザー作成リクエストをauth-apiに中継する

    リクエストボディからユーザー情報を取得して、
    auth-apiにユーザー作成処理を委譲する
    
    """
    try:
        response = requests.post(
        "http://localhost:8004/auth/signup",
        json=user_create.model_dump()
    )
    except RequestException:
        handle_requesterror('auth-api')
    raise_if_error_response(response,'auth-api')
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
    try:
        response = requests.post(
        f"http://localhost:8003/order?product_id={product_id}&quantity={quantity}",
        headers={'Authorization':authorization}
    )
    except RequestException:
        handle_requesterror('order-api')
    raise_if_error_response(response,'order-api')
    return response.json()