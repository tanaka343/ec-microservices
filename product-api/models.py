from ..base import Base
from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship


class Item(Base):
    __tablename__ = "products"
    id = Column(Integer,primary_key=True)
    name = Column(String,nullable=False)
    price = Column(String,nullable=False)
    detail = Column(String,nullable=True)
    category_id = Column(Integer,ForeignKey("categories.id",name="fk_ctegory_id",ondelete="CASCADE"),nullable=False)
    category = relationship("Category",back_populates="products")

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer,primary_key=True)
    category_name = Column(String,nullable=False)
    products = relationship("Item",back_populates="category")