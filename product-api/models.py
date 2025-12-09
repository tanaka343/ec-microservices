from database import Base
from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship


class Item(Base):
    __tablename__ = "products"
    id = Column(Integer,primary_key=True)
    name = Column(String,nullable=False)
    price = Column(String,nullable=False)
    detail = Column(String,nullable=True)

    

