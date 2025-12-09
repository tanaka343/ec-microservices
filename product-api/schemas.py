from pydantic import BaseModel,Field,ConfigDict
from typing import Optional


class ItemCreate(BaseModel):
    name :str = Field(min_length=2,max_length=20,examples=["tanaka"])
    email :str = Field(examples=["email@com"])


class ItemUpdate(BaseModel):
    name : Optional[str] = Field(default=None,min_length=2,max_length=20,examples=["yamada"])
    email : Optional[str] = Field(default=None,examples=["email@com"])


class ItemResponse(BaseModel):
    id :int
    name :str = Field(min_length=2,max_length=20,examples=["satou"])
    email :str = Field(min_length=2,max_length=20,examples=["dafgz@com"])
    user_id :int
    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    name : str = Field(min_length=2,examples=["tanaka"])
    password : str = Field(min_length=8,examples=["test1234"])

class UserResponse(BaseModel):
    id : int = Field(gt=0,examples=["1"])
    name : str = Field(min_length=2,examples=["yamada"])
    
    model_config= ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token :str
    token_type :str

class Decoded_Token(BaseModel):
    username : str
    user_id : int