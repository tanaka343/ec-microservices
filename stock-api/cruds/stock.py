from sqlalchemy.orm import Session
from models import stock
from schemas import StockCreate,StockUpdate

class ProductNotFoundError(Exception):
    """商品が見つからない"""
    pass

def find_all(db: Session):
  return db.query(stock).all()


def find_by_id(product_id: int,db :Session):
  item = db.query(stock).filter(stock.product_id==product_id).first()
  if not item:
    raise ProductNotFoundError(f'商品ID：{product_id}が見つかりません')
  return item

def create(db :Session,create_stock :StockCreate):
  new_item = stock(
    **create_stock.model_dump()
  )
  db.add(new_item)
  db.commit()
  return new_item

def update(product_id :int,db :Session,update_stock :StockUpdate):
  item = find_by_id(product_id,db)
  item.stock =item.stock if update_stock.stock is None else update_stock.stock
  db.add(item)
  db.commit()
  return item


def delete(product_id :int,db :Session):
  delete_item = find_by_id(product_id,db)
  db.delete(delete_item)
  db.commit()
  return delete_item