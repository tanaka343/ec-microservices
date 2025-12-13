from sqlalchemy.orm import Session
from schemas import CreateUser
from models import User
import base64
import os
import hashlib

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