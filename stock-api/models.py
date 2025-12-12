from sqlalchemy import Column,Integer,ForeignKey
from database import Base

class stock(Base):
  __tablename__ = "stocks"
  id = Column(Integer,primary_key=True)
  product_id = Column(Integer,unique=True)
  stock = Column(Integer,nullable=False)