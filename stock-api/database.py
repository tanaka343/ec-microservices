from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

SQLALCHEMY_URL = "sqlite:///../stock.db"

engine = create_engine(SQLALCHEMY_URL)

SessionLocal = sessionmaker(bind=engine,autoflush=False,autocommit=False)


def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()