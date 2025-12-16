from fastapi import FastAPI,Depends
import requests
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

app = FastAPI()
FormDependency = Annotated[OAuth2PasswordBearer,Depends()]

@app.get("/")
def top():
    return "hello "


@app.get("/products")
def get_products():
    response = requests.get(
        "http://localhost:8001/products"
    )
    return response.json()

@app.get("/login")
def login(username,password):
    response = requests.post(
        "http://localhost:8003/auth/login",
        data={'username':username,'password':password}
    )
    return response.json()