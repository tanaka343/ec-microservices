from fastapi import APIRouter,Depends
from schemas import CreateUser
from typing import Annotated
from sqlalchemy.orm import Session
from database import get_db
from cruds import auth as auth_cruds
from schemas import ResponseUser,Token
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

router = APIRouter(prefix="/auth",tags=["auth"])
DbDependency = Annotated[Session,Depends(get_db)]
FormDependency = Annotated[OAuth2PasswordRequestForm,Depends()]

@router.post("/signup",response_model=ResponseUser)
def create_user(db :DbDependency,user_create :CreateUser):
    return auth_cruds.create_user(db,user_create)

@router.post("/login",response_model=Token)
def login(db :DbDependency,form_data :FormDependency):
    user_name = form_data.username
    password = form_data.password
    user = auth_cruds.login(db,user_name,password)
    token = auth_cruds.create_access_token(user.user_name,user.id,timedelta(minutes=20))
    return {"access_token":token,"token_type":"bearer"}