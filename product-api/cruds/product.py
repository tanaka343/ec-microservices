from fastapi import Depends
from database import get_db
from sqlalchemy.orm import Session
from models import Item
from schemas import ItemCreate,ItemUpdate

class ProductNotFoundError(Exception):
    """商品が見つからない"""
    pass

def find_all(db :Session ):
    return db.query(Item).order_by(Item.id).all()

def find_by_id(id :int,db :Session ):
    item = db.query(Item).filter(Item.id == id).first()
    if not item:
        raise ProductNotFoundError(f'商品ID：{id}が見つかりません')
    return item

def find_by_name(name :str,db :Session):
    item = db.query(Item).filter(Item.name == name).all()
    if not item:
        raise ProductNotFoundError(f'商品名：{name}が見つかりません')

def create(create_item :ItemCreate,db :Session):

    new_item = Item(
    **create_item.model_dump()
    )
    db.add(new_item)
    db.commit()
    return new_item

   
def update(id :int,update_item :ItemUpdate,db :Session):
    item = find_by_id(id,db)
    
    item.name =item.name if update_item.name is None else update_item.name
    item.price =item.price if update_item.price is None else update_item.price
    item.detail =item.detail if update_item.detail is None else update_item.detail
    item.status =item.status if update_item.status is None else update_item.status
    item.category_id =item.category_id if update_item.category_id is None else update_item.category_id
    
    db.add(item)
    db.commit()
    return item

def deleate(id :int,db :Session):
    item = find_by_id(id,db)
    db.delete(item)
    db.commit()
    return item