from typing import Optional
from pydantic import BaseModel,Field

class CreateUser(BaseModel):
    user_name : str = Field(min_length=2,max_length=20,examples=["user1"])
    password : str = Field(min_length=8,max_length=20,examples=["password1234"])

class ItemCreate(BaseModel):
    name :str = Field(min_length=2,max_length=20,examples=["desk"])
    price :str = Field(examples=["2000"])
    detail :str = Field(min_length=2,max_length=50,examples=["学習机です。"])
    status : bool = Field(default=True,examples=[True])
    category_id :int = Field(examples=["1"])

class ItemUpdate(BaseModel):
    name :Optional[str] = Field(default=None,min_length=2,max_length=20,examples=["desk"])
    price :Optional[str] = Field(default=None,examples=["2000"])
    detail :Optional[str] = Field(default=None,min_length=2,max_length=50,examples=["学習机です。"])
    status : Optional[bool] = Field(default=None,examples=[True])
    category_id :Optional[int] = Field(default=None,examples=["1"])

class StockCreate(BaseModel):
    product_id :int = Field(examples=["1"])
    stock :int = Field(examples=["10"])

class StockUpdate(BaseModel):
    stock :int = Field(examples=["5"])

