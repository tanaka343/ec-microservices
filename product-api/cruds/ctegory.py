from sqlalchemy.orm import Session
from models import Item,Category
from schemas import CategoryCreate,CategoryUpdate

def find_all(db: Session):
  return db.query(Category).all()


def find_by_id(id: int,db :Session):
  found_item = db.query(Category).filter(Category.id==id).first()
  if not found_item:
    return None
  return found_item


def create(db :Session,create_category :CategoryCreate):
  new_item = Category(
    **create_category.model_dump()
  )
  db.add(new_item)
  db.commit()
  return new_item

def update(id :int,db :Session,update_category :CategoryUpdate):
  update_item = find_by_id(id,db)
  if not update_item:
    return None
  update_item.category_name =update_item.category_name if update_category.category_name is None else update_category.category_name
  db.add(update_item)
  db.commit()
  return update_item


def delete(id :int,db :Session):
  delete_item = find_by_id(id,db)
  if not delete_item:
    return None
  db.delete(delete_item)
  db.commit()
  return delete_item