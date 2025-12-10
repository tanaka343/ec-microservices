from sqlalchemy.orm import Session
from models import Item,Category
from schemas import CategoryCreate,CategoryUpdate

def find_all(db: Session):
  return db.query(Category).all()


def find_by_id(id: int,db :Session):
  return db.query(Category).filter(Category.id==id).first()


def create(db :Session,create_category :CategoryCreate):
  new_category = Category(
    **create_category.model_dump()
  )
  db.add(new_category)
  db.commit()
  return new_category

def update(id :int,db :Session,update_category :CategoryUpdate):
  item = find_by_id(id,db)
  item.category_name =item.category_name if update_category.category_name is None else update_category.category_name
  db.add(item)
  db.commit()
  return item


def delete(id :int,db :Session):
  delete_category = find_by_id(id,db)
  db.delete(delete_category)
  db.commit()
  return delete_category