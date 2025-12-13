from fastapi import APIRouter,Depends,HTTPException
from database import get_db
from sqlalchemy.orm import Session
from typing import Annotated
from cruds import stock as stock_cruds
from schemas import StockCreate,StockResponse,StockUpdate
from starlette import status

router = APIRouter(prefix="/stock",tags=["stock"])

Dbdependency = Annotated[Session,Depends(get_db)]

@router.get("",response_model=list[StockResponse],status_code=status.HTTP_200_OK)
async def find_all(db :Dbdependency):
  return stock_cruds.find_all(db)

@router.get("/{product_id}",response_model=StockResponse,status_code=status.HTTP_200_OK)
async def find_by_id(product_id :int,db :Dbdependency):
  found_item = stock_cruds.find_by_id(product_id,db)
  if not found_item:
    raise HTTPException(status_code=404,detail=f"商品ID:{product_id}が見つかりません。")
  return found_item

@router.post("",response_model=StockResponse,status_code=status.HTTP_201_CREATED)
async def create(db :Dbdependency,create_stock :StockCreate):
  return stock_cruds.create(db,create_stock)

@router.put("/{product_id}",response_model=StockResponse,status_code=status.HTTP_200_OK)
async def update(product_id :int,db :Dbdependency,update_category :StockUpdate):
  update_item = stock_cruds.update(product_id,db,update_category)
  if not update_item:
    raise HTTPException(status_code=404,detail=f"商品ID:{product_id}が見つかりません。")
  return update_item

@router.delete("/{product_id}",response_model=StockResponse,status_code=status.HTTP_200_OK)
async def delete(product_id :int,db :Dbdependency):
  delete_item = stock_cruds.delete(product_id,db)
  if not delete_item:
    raise HTTPException(status_code=404,detail=f"商品ID:{product_id}が見つかりません。")
  return delete_item