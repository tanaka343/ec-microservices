from fastapi import APIRouter,Depends,HTTPException
from database import get_db
from sqlalchemy.orm import Session
from typing import Annotated
from cruds import stock as stock_cruds
from schemas import StockCreate,StockResponse,StockUpdate
from starlette import status
from cruds.stock import ProductNotFoundError

router = APIRouter(prefix="/stock",tags=["stock"])

Dbdependency = Annotated[Session,Depends(get_db)]

@router.get("",response_model=list[StockResponse],status_code=status.HTTP_200_OK)
async def find_all(db :Dbdependency):
  return stock_cruds.find_all(db)

@router.get("/{product_id}",response_model=StockResponse,status_code=status.HTTP_200_OK)
async def find_by_id(product_id :int,db :Dbdependency):
  try:
    return stock_cruds.find_by_id(product_id,db)
  except ProductNotFoundError as e:
    raise HTTPException(status_code=404,detail=str(e))
  

@router.post("",response_model=StockResponse,status_code=status.HTTP_201_CREATED)
async def create(db :Dbdependency,create_stock :StockCreate):
  return stock_cruds.create(db,create_stock)

@router.put("/{product_id}",response_model=StockResponse,status_code=status.HTTP_200_OK)
async def update(product_id :int,db :Dbdependency,update_stock :StockUpdate):
  try:
    return stock_cruds.update(product_id,db,update_stock)
  except ProductNotFoundError as e:
    raise HTTPException(status_code=404,detail=str(e))

@router.delete("/{product_id}",response_model=StockResponse,status_code=status.HTTP_200_OK)
async def delete(product_id :int,db :Dbdependency):
  try:
    return stock_cruds.delete(product_id,db)
  except ProductNotFoundError as e:
    raise HTTPException(status_code=404,detail=str(e))