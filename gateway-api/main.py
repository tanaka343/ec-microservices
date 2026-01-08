from fastapi import FastAPI,Depends,APIRouter
import requests
from fastapi.security import OAuth2PasswordRequestForm,APIKeyHeader
from typing import Annotated,Optional
from pydantic import BaseModel,Field
from schemas import CreateUser,ItemCreate,ItemUpdate,StockCreate,StockUpdate

app = FastAPI()
FormDependency = Annotated[OAuth2PasswordRequestForm,Depends()]
api_key_header = APIKeyHeader(name="Authorization")



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

@app.post("/login",tags=['auth'])
def login(form_data:FormDependency):
    username=form_data.username
    password=form_data.password
    response = requests.post(
        f"https://auth-api-987336615042.asia-northeast1.run.app/auth/login",
        data={'username':username,'password':password}
    )
    return response.json()

@app.post("/signup",tags=['auth'])
def signup(user_create :CreateUser):
    response = requests.post(
        f"https://auth-api-987336615042.asia-northeast1.run.app/auth/signup",
        json=user_create.model_dump()
    )
    return response.json()

@app.post("/order",tags=['order'])
def order(product_id:int,quantity:int,authorization: str = Depends(api_key_header)):
    response = requests.post(
        f"https://order-api-987336615042.asia-northeast1.run.app/order?product_id={product_id}&quantity={quantity}",
        headers={'Authorization':authorization}
    )
    return response.json()