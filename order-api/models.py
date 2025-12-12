from database import Base
from datetime import datetime
from sqlalchemy import Column,Integer,String,DateTime

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer,primary_key=True)
    product_id = Column(Integer,nullable=False)
    quantity = Column(Integer,nullable=False)
    order_at = Column(DateTime,default=datetime.now())