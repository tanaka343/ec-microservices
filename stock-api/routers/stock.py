from fastapi import APIRouter,Depends
from database import get_db
from sqlalchemy.orm import Session
from typing import Annotated
from cruds import stock as stock_cruds
from schemas import StockCreate,StockResponse,StockUpdate

router = APIRouter(prefix="/stock",tags=["stock"])

Dbdependency = Annotated[Session,Depends(get_db)]

@router.get("",response_model=list[StockResponse])
async def find_all(db :Dbdependency):
  return stock_cruds.find_all(db)

@router.get("/id",response_model=StockResponse)
async def find_by_id(product_id :int,db :Dbdependency):
  return stock_cruds.find_by_id(product_id,db)

@router.post("",response_model=StockResponse)
async def create(db :Dbdependency,create_stock :StockCreate):
  return stock_cruds.create(db,create_stock)

@router.put("",response_model=StockResponse)
async def update(product_id :int,db :Dbdependency,update_category :StockUpdate):
  return stock_cruds.update(product_id,db,update_category)

@router.delete("",response_model=StockResponse)
async def delete(product_id :int,db :Dbdependency):
  return stock_cruds.delete(product_id,db)