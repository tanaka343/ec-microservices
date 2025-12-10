from fastapi import Depends
from database import get_db
from sqlalchemy.orm import Session
from models import Item
from schemas import ItemCreate,ItemUpdate


def find_all(db :Session ):
    return db.query(Item).order_by(Item.id).all()

def find_by_id(id :int,user_id :int,db :Session ):
   return db.query(Item).filter(Item.id == id).filter(Item.user_id ==user_id).first()

def find_by_name(name :str,db :Session):
    return db.query(Item).filter(Item.name == name).all()

def create(create_item :ItemCreate,user_id :int,db :Session):

    new_item = Item(
    **create_item.model_dump(),user_id=user_id
    )
    db.add(new_item)
    db.commit()
    return new_item

   
def update(id :int,update_item :ItemUpdate,user_id :int,db :Session):
    item = db.query(Item).filter(Item.id == id).filter(Item.user_id==user_id).first()
    
    if item is None:
        return None
    
    item.name =item.name if update_item.name is None else update_item.name
    item.price =item.price if update_item.price is None else update_item.price
    item.email =item.detail if update_item.detail is None else update_item.detail
    item.email =item.category_id if update_item.category_id is None else update_item.category_id
    
    db.add(item)
    db.commit()
    return item

def deleate(id :int,user_id :int,db :Session):
    item = find_by_id(id,user_id,db)
    if item is None:
       return None
    db.delete(item)
    db.commit()
    return item