from fastapi import APIRouter,Depends,HTTPException
from database import get_db
from sqlalchemy.orm import Session
from typing import Annotated
from cruds import order as order_cruds
from schemas import OrderResponse
from starlette import status
from fastapi.security import OAuth2PasswordBearer,APIKeyHeader
from jose import jwt

router = APIRouter(prefix="/order",tags=["order"])

Dbdependency = Annotated[Session,Depends(get_db)]
oath2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")
SECRET_KEY = "3FIQodO54obEzChoXmZFaprULmWd1KkYqc5GbITvYwA="
ALGORISM = "HS256"
api_key_header = APIKeyHeader(name="Authorization")

@router.post("",response_model=OrderResponse,status_code=status.HTTP_201_CREATED)
async def order_confirm(db :Dbdependency,product_id :int,quantity :int,authorization: str = Depends(api_key_header)):
  """JWT検証をして注文を確定するAPIエンドポイント

  JWT検証を行って、正常な場合は注文確定処理を実行する
  業務例外はHTTPエラーに変換して返却する

  Args:
        db: データベースセッション
        product_id: 商品ID
        quantity: 注文数
        authorization: Bearerトークン
        
    Returns:
        new_order: 作成された注文情報
        
    Raises:
        HTTPException:
            - トークンが不正な場合
            - 商品が存在しない場合
            - 商品が販売中止の場合
            - 在庫が不足している場合
  """
  token = authorization.replace("Bearer ", "")
  try:
    payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORISM)
    user_id = payload["id"]
  except:
    raise HTTPException(status_code=404,detail="不正なトークンです。")
  try:
    return await order_cruds.order_confirm(db,product_id,quantity,user_id)
  
  except order_cruds.ProductNotFoundError as e:
    raise HTTPException(status_code=400,detail=str(e))
  except order_cruds.InsufficientStockError as e:
    raise HTTPException(status_code=400,detail=str(e))
  except order_cruds.ProductDiscontinuedError as e:
    raise HTTPException(status_code=400,detail=str(e))