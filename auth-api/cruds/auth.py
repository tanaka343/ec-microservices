from sqlalchemy.orm import Session
from schemas import CreateUser,DecodedToken
from models import User
import base64
import os
import hashlib
from datetime import timedelta,datetime
from jose import JWTError,jwt
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

class UserAlreadyExistsError(Exception):
    """ユーザーが既に存在"""
    pass
class InvalidCredentialsError(Exception):
    """認証情報が不正"""
    pass
class InvalidTokenError(Exception):
    """トークンが不正"""
    pass

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
    try:
        db.add(new_user)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise UserAlreadyExistsError(f'ユーザー名：{user_create.user_name}は既に使用されています')
    return new_user

def login(db :Session,user_name :str,password :str):
    user = db.query(User).filter(User.user_name==user_name).first()
    if not user:
        raise InvalidCredentialsError(f'ユーザー名が正しくありません')
    hashed_password = hashlib.pbkdf2_hmac("sha256",password.encode(),user.salt.encode(),1000).hex()

    if user.password != hashed_password:
        raise InvalidCredentialsError(f'パスワードが正しくありません')
    return user


def create_access_token(user_name :str,user_id :int,expires_delta :timedelta):
    expires = datetime.now() + expires_delta
    payload = {"sub" :user_name,"id" :user_id,"exp" :expires}
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORISM)

oath2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")
def get_current_user(token :Annotated[str,Depends(oath2_schema)]):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithm=ALGORISM)
        user_name = payload.get("sub")
        user_id = payload.get("id")
        if user_name is None or user_id is None:
            raise InvalidTokenError(f'トークンが不正です')
        return DecodedToken(user_name=user_name,user_id=user_id)
    except JWTError as e:
        raise InvalidTokenError(f'JWT検証に失敗しました') from e
