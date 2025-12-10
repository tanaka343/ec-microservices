from fastapi import APIRouter,Depends
from database import get_db
from sqlalchemy.orm import Session
from typing import Annotated
from cruds import ctegory as category_cruds
from schemas import CategoryResponse,CategoryCreate,CategoryUpdate

router = APIRouter(prefix="/category",tags=["category"])

Dbdependency = Annotated[Session,Depends(get_db)]

@router.get("",response_model=list[CategoryResponse])
async def find_all(db :Dbdependency):
  return category_cruds.find_all(db)

@router.get("/id",response_model=CategoryResponse)
async def find_by_id(id :int,db :Dbdependency):
  return category_cruds.find_by_id(id,db)

@router.post("",response_model=CategoryResponse)
async def create(db :Dbdependency,create_category :CategoryCreate):
  return category_cruds.create(db,create_category)

@router.put("",response_model=CategoryResponse)
async def update(id :int,db :Dbdependency,update_category :CategoryUpdate):
  return category_cruds.update(id,db,update_category)

@router.delete("",response_model=CategoryCreate)
async def delete(id :int,db :Dbdependency):
  return category_cruds.delete(id,db)