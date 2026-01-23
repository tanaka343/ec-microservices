from fastapi import APIRouter,Depends,HTTPException
from database import get_db
from schemas import ItemResponse,ItemCreate,ItemUpdate
from sqlalchemy.orm import Session
from typing import Annotated,Optional
from starlette import status
from cruds import product as product_cruds
from cruds.product import ProductNotFoundError


router = APIRouter(prefix="/products",tags=["products"])

DbDependency = Annotated[Session,Depends(get_db)]

@router.get("",response_model=list[ItemResponse],status_code=status.HTTP_200_OK)
async def find_all(db :DbDependency):
    return product_cruds.find_all(db)

@router.get("/{id}",response_model=Optional[ItemResponse],status_code=status.HTTP_200_OK)
async def find_by_id(id :int,db :Session = Depends(get_db)):
    try:
       return product_cruds.find_by_id(id,db)
    except ProductNotFoundError as e:
       raise HTTPException(status_code=404,detail=str(e))
   
@router.get("",response_model=list[ItemResponse],status_code=status.HTTP_200_OK)
async def find_by_name(name :str,db :DbDependency):
    try:
        product_cruds.find_by_name(name,db)
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404,detail=str(e))


@router.post("",response_model=ItemResponse,status_code=status.HTTP_201_CREATED)
async def create(create_item :ItemCreate,db :DbDependency):
    new_item = product_cruds.create(create_item,db)
    return new_item


@router.put("/{id}",response_model=Optional[ItemResponse],status_code=status.HTTP_200_OK)
async def update(id :int,update_item :ItemUpdate,db :DbDependency):
    try:
        return product_cruds.update(id,update_item,db)
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404,detail=str(e))
    
            
        
@router.delete("/{id}",response_model=Optional[ItemResponse],status_code=status.HTTP_200_OK)
async def deleate(id :int,db :DbDependency):
    try:
        return product_cruds.deleate(id,db)
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404,detail=str(e))
    