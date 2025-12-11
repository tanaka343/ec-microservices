from sqlalchemy import Column,Integer,ForeignKey
from ..base import Base

class stock(Base):
  __tablename__ = "stocks"
  id = Column(Integer,primary_key=True)
  product_id = Column(Integer,ForeignKey("products.id",name="fk_products_id",ondelete="CASCADE"),unique=True)
  stock = Column(Integer,nullable=False)