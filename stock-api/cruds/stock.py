from sqlalchemy.orm import Session
from models import stock
from schemas import StockCreate,StockUpdate

def find_all(db: Session):
  return db.query(stock).all()


def find_by_id(product_id: int,db :Session):
  return db.query(stock).filter(stock.product_id==product_id).first()


def create(db :Session,create_stock :StockCreate):
  new_item = stock(
    **create_stock.model_dump()
  )
  db.add(new_item)
  db.commit()
  return new_item

def update(product_id :int,db :Session,update_stock :StockUpdate):
  item = find_by_id(product_id,db)
  if not item:
    return None
  item.stock =item.stock if update_stock.stock is None else update_stock.stock
  db.add(item)
  db.commit()
  return item


def delete(product_id :int,db :Session):
  delete_item = find_by_id(product_id,db)
  if not delete_item:
    return None
  db.delete(delete_item)
  db.commit()
  return delete_item