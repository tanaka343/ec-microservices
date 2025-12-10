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

class CategoryResponse(BaseModel):
    id : int = Field(gt=0)
    category_name :str = Field(min_length=2,max_length=20)
