from sqlalchemy.orm import Session
from schemas import CreateUser
from models import User
import base64
import os
import hashlib
from datetime import timedelta,datetime
from jose import JWTError,jwt

def create_user(db :Session,user_create :CreateUser):
    salt = base64.b64encode(os.urandom(32))
    # os.urandom(32) を使用して、32バイトのランダムなバイト列を生成
    # base64.b64encode() を使用して、このランダムなバイト列をASCII文字列に符号化
    hashed_password = hashlib.pbkdf2_hmac("sha256",user_create.password.encode(),salt,1000).hex()
    # エンコードしたパスワード+saltをハッシュアルゴリズムの形式（SHA-256）で１０００回ハッシュ化
    # ハッシュ結果のバイト列を16進数文字列（.hex()）に変換
    new_user=User(
        user_name = user_create.user_name,
        password = hashed_password,
        salt = salt.decode()
    )
    db.add(new_user)
    db.commit()
    return new_user

def login(db :Session,user_name :str,password :str):
    user = db.query(User).filter(User.user_name==user_name).first()
    if not user:
        return None
    hashed_password = hashlib.pbkdf2_hmac("sha256",password.encode(),user.salt.encode(),1000).hex()

    if user.password != hashed_password:
        return None
    return user

SECRET_KEY = "3FIQodO54obEzChoXmZFaprULmWd1KkYqc5GbITvYwA="
ALGORISM = "HS256"
def create_access_token(user_name :str,user_id :int,expires_delta :timedelta):
    expires = datetime.now() + expires_delta
    payload = {"sub" :user_name,"id" :user_id,"exp" :expires}
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORISM)

