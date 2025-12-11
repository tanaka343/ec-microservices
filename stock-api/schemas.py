from pydantic import Field,BaseModel,ConfigDict

class ItemCreate(BaseModel):
    product_id :int = Field(examples=["1"])
    stock :int = Field(examples=["10"])


class ItemUpdate(BaseModel):
    product_id :int = Field(examples=["1"])
    stock :int = Field(examples=["5"])


class ItemResponse(BaseModel):
    id :int
    product_id :int = Field(examples=["1"])
    stock :int = Field(examples=["10"])

    model_config = ConfigDict(from_attributes=True)#ORMオブジェクト（属性を持つクラスインスタンス）をPydanticモデルに変換する