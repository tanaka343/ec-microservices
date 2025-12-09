from fastapi import APIRouter,Depends,HTTPException
from models import Item
from database import get_db
from schemas import ItemResponse,ItemCreate,ItemUpdate,Decoded_Token
from sqlalchemy.orm import Session
from typing import Annotated,Optional
from starlette import status
from cruds import item as item_cruds
from cruds import auth as auth_cruds

router = APIRouter(prefix="/items",tags=["items"])

DbDependency = Annotated[Session,Depends(get_db)]
userDependency = Annotated[Decoded_Token,Depends(auth_cruds.get_current_user)]

@router.get("",response_model=list[ItemResponse],status_code=status.HTTP_200_OK)
async def find_all(db :DbDependency):
    return item_cruds.find_all(db)

@router.get("/{id}",response_model=Optional[ItemResponse],status_code=status.HTTP_200_OK)
async def find_by_id(id :int,user :userDependency,db :Session = Depends(get_db)):
   found_item = item_cruds.find_by_id(id,user.user_id,db)
   if found_item is None:
       raise HTTPException(status_code=404,detail="Item not found")
   return found_item
       

@router.get("/",response_model=list[ItemResponse],status_code=status.HTTP_200_OK)
async def find_by_name(name :str,db :DbDependency):
    found_item = item_cruds.find_by_name(name,db)
    if not found_item:
        raise HTTPException(status_code=404,detail="Item not found")
    return found_item


@router.post("",response_model=ItemResponse,status_code=status.HTTP_201_CREATED)
async def create(create_item :ItemCreate,user :userDependency,db :DbDependency):
    new_item = item_cruds.create(create_item,user.user_id,db)
    return new_item


@router.put("/{id}",response_model=Optional[ItemResponse],status_code=status.HTTP_200_OK)
async def update(id :int,update_item :ItemUpdate,user :userDependency,db :DbDependency):
    item = item_cruds.update(id,update_item,user.user_id,db)
    if item is None:
        raise HTTPException(status_code=404,detail="Item not found")
    return item
            
        
@router.delete("/{id}",response_model=Optional[ItemResponse],status_code=status.HTTP_200_OK)
async def deleate(id :int,user :userDependency,db :DbDependency):
    item = item_cruds.deleate(id,user.user_id,db)
    if item is None:
        raise HTTPException(status_code=404,detail="Item not found")
    return item