# 注文システム　マイクロサービス

FastAPIを使用したEcサイトの注文システムのマイクロサービス実装例です。\
各サービスは独立しており、サービス間通信にはREST APIを使用しています。
注文確定時にイベントを発生させ、後続の処理をする仕組みをいれました。

## 目的

- マイクロサービスアーキテクチャの理解と実装
- サービス間通信（REST API）の実装
- イベント駆動での連携理解と実装
- 同期非同期通信の理解
- メッセージキューの導入

## 技術スタック

FastAPI\
SQLAlchemy（ORM）\
Alembic（マイグレーション）\
SQLite\
Pydantic（バリデーション）\
python-jose（JWT 認証）\
redis（メッセージキュー）\

## ファイル構成

```python
ec-microservice/
├── auth-api/          # 認証サービス
├── product-api/       # 商品管理サービス
├── stock-api/         # 在庫管理サービス
├── order-api/         # 注文サービス
├── requirements.txt   # 共通依存パッケージ
└── README.md          # このファイル
```

## 各サービスの役割

### Auth API（認証サービス）

- 画面表示
- ユーザー操作
- JWT を使ってFastAPIと通信

### Product API（商品管理サービス）

- 認証（JWT）
- DB操作
- タスクのCRUD

## Stock API（在庫管理サービス）


## Order API（注文サービス）



## セットアップ

### 1. 依存パッケージのインストール

```bash
pip install -r ../requirements.txt

```

### 2. 各サービスのデータベースセットアップ

```bash
# Auth API
cd auth-api
alembic upgrade head

# Product API
cd ../product-api
alembic upgrade head

# Stock API
cd ../stock-api
alembic upgrade head

# Order API
cd ../order-api
alembic upgrade head
```

### 実行方法

各サービスを別々のターミナルで起動してください。

```bash
# Auth API
cd auth-api
python main.py
# → http://localhost:8004

# Product API
cd product-api
python main.py
# → http://localhost:8001

# Stock API
cd stock-api
python main.py
# → http://localhost:8002

# Order API
cd order-api
python main.py
# → http://localhost:8003
```

各サービスは自動生成されるSwagger UIでAPIを確認できます。

- Auth API: <http://localhost:8000/docs>
- Product API: <http://localhost:8001/docs>
- Stock API: <http://localhost:8002/docs>
- Order API: <http://localhost:8003/docs>

## API 使用例

### ユーザー登録
   
```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"user_name": "testuser", "password": "testpass1234"}'
```

### ログイン（JWT取得）

```bash
curl -X POST http://localhost:8000/auth/login \
  -d "username=testuser&password=testpass1234"

# レスポンス例
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 商品登録（Product API）

```bash
curl -X POST http://localhost:8001/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "デスク",
    "price": "15000",
    "detail": "木製の学習机",
    "category_id": 1
  }'
```

### 在庫登録（Stock API）

```bash
curl -X POST http://localhost:8002/stock \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "stock": 50
  }'
```

### 注文（Order API - JWT必須）

```bash
curl -X POST "http://localhost:8003/order?product_id=1&quantity=2" \
  -H "Authorization: Bearer {JWT_TOKEN}"
```





## 工夫した点・学んだこと


## 改善点・今後の課題

