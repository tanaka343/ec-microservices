from pydantic import BaseModel,Field,ConfigDict
from typing import Optional


class ItemCreate(BaseModel):
    name :str = Field(min_length=2,max_length=20,examples=["desk"])
    price :str = Field(examples=["2000"])
    detail :str = Field(min_length=2,max_length=50,examples=["学習机です。"])
    category_id :int = Field(examples=["1"])


class ItemUpdate(BaseModel):
    name :Optional[str] = Field(min_length=2,max_length=20,examples=["desk"])
    price :Optional[str] = Field(examples=["2000"])
    detail :Optional[str] = Field(min_length=2,max_length=50,examples=["学習机です。"])
    category_id :Optional[int] = Field(examples=["1"])


class ItemResponse(BaseModel):
    id :int
    name :str = Field(min_length=2,max_length=20,examples=["desk"])
    price :str = Field(examples=["2000"])
    detail :str = Field(min_length=2,max_length=50,examples=["学習机です。"])
    category_id :int = Field(examples=["1"])

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