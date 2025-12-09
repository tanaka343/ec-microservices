from fastapi import FastAPI,Body,Depends,HTTPException,Request
from schemas import ItemCreate,ItemUpdate,ItemResponse,UserCreate,UserResponse,Token,Decoded_Token
from database import get_db
from typing import Optional,Annotated
from sqlalchemy.orm import Session
from models import Item,User
from starlette import status
import hashlib
import base64
import os
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from datetime import timedelta,datetime
from jose import jwt,JWTError
from fastapi.security import OAuth2PasswordBearer

from routers import item,auth

app = FastAPI()
app.include_router(item.router)
app.include_router(auth.router)

# デバック用
@app.exception_handler(RequestValidationError)
async def handler(request:Request, exc:RequestValidationError):
    print(exc)
    return JSONResponse(content={}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
