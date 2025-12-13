
from pydantic import BaseModel,Field
from datetime import datetime

class OrderCreate(BaseModel):
    product_id : int = Field(examples=["1"])
    quantity : int = Field(gt=0,examples=["1"])
    order_at : datetime

class OrderResponse(BaseModel):
    id : int =Field(examples=["1"])
    product_id : int = Field(examples=["1"])
    quantity : int = Field(gt=0,examples=["1"])
    order_at : datetime