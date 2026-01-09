import redis
import json
import aiohttp
import asyncio

# Redisの購読設定
redis_client = redis.Redis(host='localhost',port=6379,decode_responses=True)
pubsub = redis_client.pubsub()
pubsub.subscribe("order_confirmed")

print(f'イベント購読開始：order_confirmed')

# 外部接続
async def update_stock(product_id :int,new_stock :int):
    """在庫の更新を外部APIに依頼する

    外部APIにアクセスして在庫情報を更新する
    更新を失敗した場合は、レスポンスをテキストで出力し、イベント処理全体は継続する

    Args:
        product_id: 商品ID
        new_stock: 在庫数－注文数
        
    """
    async with aiohttp.ClientSession() as session:
        async with session.put(
            f"http://localhost:8002/stock/{product_id}",
            json={'stock':new_stock}
            ) as response:
            if response.status == 200:
              print(f'在庫更新完了：product_id={product_id},new_stock={new_stock}')
            else:
              print(f'在庫更新失敗:{response.text}')

    
async def update_product_status(product_id :int):
    """販売状況の更新を外部APIに依頼する

    外部APIにアクセスして販売状況を更新する
    更新を失敗した場合は、エラーを出す(致命的な失敗として扱う)

    Args:
        product_id: 商品ID
        
    Raises:
        Exception: 販売状況を更新できない場合
    
    """
    async with aiohttp.ClientSession() as session:
        async with session.put(
            f"http://localhost:8001/products/{product_id}",
            json={'status':False}
            ) as response:
            if response.status ==200:
                print(f'販売中止：product_id={product_id}')
            else :
                raise Exception(f"販売状況を更新できません:status={response.status}")

async def handle_stock_update(event_data):
  """注文確定イベントを受けて、在庫数を減らす"""
  product_id = event_data['product_id']
  stock = event_data['stock']
  quantity = event_data['quantity']

  new_stock = stock-quantity
  await update_stock(product_id,new_stock)
  
async def handle_product_status(event_data):
  """在庫数が０になった場合、販売状況を販売中止にする"""
  product_id = event_data['product_id']
  stock = event_data['stock']
  quantity = event_data['quantity']
  new_stock = stock-quantity

  if new_stock == 0:
    await update_product_status(product_id)
   
HANDLERS = [
    handle_stock_update,   
    handle_product_status   
]

for message in pubsub.listen():
  # Redisからイベントを待ち受ける
  if message['type'] == 'message':
    # イベントデータを取得する
    event_data = json.loads(message['data'])
    print(f'イベント受信:{event_data}')
    async def run_handlers():
      # asyncio.runを実行するためにasync関数で包む
      # 登録されているイベントハンドラをすべて並処理する
      tasks=[handler(event_data) for handler in HANDLERS]
      await asyncio.gather(*tasks)
    # 1イベントごとに非同期処理を実行
    asyncio.run(run_handlers())# asyncio.run(何か)→渡せるのはawait関数の戻り値
