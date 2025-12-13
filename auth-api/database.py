from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

SQLALCHEMY_URL = "sqlite:///./user.db"

engine = create_engine(SQLALCHEMY_URL)

SessionLocal = sessionmaker(bind=engine,autoflush=False,autocommit=False)

Base = declarative_base()
def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()