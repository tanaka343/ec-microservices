from fastapi import APIRouter,Depends
from schemas import CreateUser
from typing import Annotated
from sqlalchemy.orm import Session
from database import get_db
from cruds import auth as auth_cruds
from schemas import ResponseUser

router = APIRouter(prefix="/auth",tags=["auth"])
DbDependency = Annotated[Session,Depends(get_db)]

@router.post("",response_model=ResponseUser)
def create_user(db : DbDependency,user_create :CreateUser):
    return auth_cruds.create_user(db,user_create)
