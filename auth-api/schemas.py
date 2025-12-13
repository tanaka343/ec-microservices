from pydantic import BaseModel,Field

class CreateUser(BaseModel):
    user_name : str = Field(min_length=2,max_length=20,examples=["user1"])
    password : str = Field(min_length=8,max_length=20,examples=["password1234"])

class ResponseUser(BaseModel):
    id : int = Field(gt=0,examples=["1"])
    user_name : str = Field(min_length=2,max_length=20,examples=["user1"])
    