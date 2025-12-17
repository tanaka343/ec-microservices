from fastapi import FastAPI,Depends,Header,HTTPException
import requests
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from jose import jwt

app = FastAPI()

oath2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")
SECRET_KEY = "3FIQodO54obEzChoXmZFaprULmWd1KkYqc5GbITvYwA="
ALGORITHM = "HS256"

@app.get("/")
def top():
    return "hello "


@app.get("/products")
def get_products():
    response = requests.get(
        "http://localhost:8001/products"
    )
    return response.json()

@app.post("/login")
def login(username :str,password :str):
    response = requests.post(
        "http://localhost:8004/auth/login",
        data={'username':username,'password':password}
    )
    return response.json()


@app.post("/order")
def create_order(
    product_id :int,
    quantity :int,
    authorization :str = Header(...)
    ):
    token = authorization.replace("Bearer ", "")
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id = payload["user_id"]
        print(f"User ID: {user_id}")
    except:
        raise HTTPException(status_code=401,detail="In valid token")
    
    response = requests.post(
         "http://localhost:8003/order",
         json={
             "product_id" :product_id,
             "quantity" :quantity,
             "user_id" :user_id
         }
    )
    print(f"Response status: {response.status_code}")  # ← 追加
    print(f"Response body: {response.text}")  # ← 追加
    return response.json()