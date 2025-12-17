from fastapi import APIRouter,Depends,HTTPException
from database import get_db
from sqlalchemy.orm import Session
from typing import Annotated
from cruds import order as order_cruds
from schemas import OrderResponse
from starlette import status
from fastapi.security import OAuth2PasswordBearer,APIKeyHeader
from jose import jwt

router = APIRouter(prefix="/order",tags=["order"])

Dbdependency = Annotated[Session,Depends(get_db)]

api_key_header = APIKeyHeader(name="Authorization")

@router.post("",response_model=OrderResponse,status_code=status.HTTP_201_CREATED)
async def create_order(db :Dbdependency,product_id :int,quantity :int,user_id :int):
  
  try:
    return order_cruds.create_order(db,product_id,quantity,user_id)
  except order_cruds.ProductNotFoundError as e:
    raise HTTPException(status_code=400,detail=str(e))
  except order_cruds.InsufficientStockError as e:
    raise HTTPException(status_code=400,detail=str(e))