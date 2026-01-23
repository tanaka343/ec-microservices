from fastapi import APIRouter,Depends,HTTPException
from database import get_db
from sqlalchemy.orm import Session
from typing import Annotated,Optional
from cruds import ctegory as category_cruds
from schemas import CategoryResponse,CategoryCreate,CategoryUpdate
from starlette import status

router = APIRouter(prefix="/category",tags=["category"])

Dbdependency = Annotated[Session,Depends(get_db)]

@router.get("",response_model=list[CategoryResponse],status_code=status.HTTP_200_OK)
async def find_all(db :Dbdependency):
  return category_cruds.find_all(db)

@router.get("/{id}",response_model=CategoryResponse,status_code=status.HTTP_200_OK)
async def find_by_id(id :int,db :Dbdependency):
  found_item = category_cruds.find_by_id(id,db)
  if not found_item:
    raise HTTPException(status_code=400,detail=f"カテゴリーID:{id}が見つかりません。")

@router.post("",response_model=CategoryResponse,status_code=status.HTTP_201_CREATED)
async def create(db :Dbdependency,create_category :CategoryCreate):
  return category_cruds.create(db,create_category)

@router.put("/{id}",response_model=CategoryResponse,status_code=status.HTTP_200_OK)
async def update(id :int,db :Dbdependency,update_category :CategoryUpdate):
  update_item = category_cruds.update(id,db,update_category)
  if not update_item:
    raise HTTPException(status_code=400,detail=f"カテゴリーID:{id}が見つかりません。")
  return update_item

@router.delete("/{id}",response_model=Optional[CategoryResponse],status_code=status.HTTP_200_OK)
async def delete(id :int,db :Dbdependency):
  delete_item = category_cruds.delete(id,db)
  if not delete_item:
    raise HTTPException(status_code=400,detail=f"カテゴリーID:{id}が見つかりません。")
  return delete_item