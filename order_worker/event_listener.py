import redis
import json
import aiohttp
import asyncio
from google.cloud import pubsub_v1
# redisから受信
# redis_client = redis.Redis(host='localhost',port=6379,decode_responses=True)
# pubsub = redis_client.pubsub()
# pubsub.subscribe("order_confirmed")

#GCP,pub/sub
project_id = 'ec-microservices-demo'
subscription_id = 'order-confirmed-sub'

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
            f"https://stock-api-987336615042.asia-northeast1.run.app/stock/{product_id}",
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
            f"https://product-api-987336615042.asia-northeast1.run.app/products/{product_id}",
            json={'status':False}
            ) as response:
            if response.status ==200:
                print(f'販売中止：product_id={product_id}')
            else :
                raise Exception(f"販売状況を更新できません:status={response.status}")

# async def handle_stock_update(event_data):
#   product_id = event_data['product_id']
#   stock = event_data['stock']
#   quantity = event_data['quantity']

#   new_stock = stock-quantity
#   await update_stock(product_id,new_stock)
  
# async def handle_product_status(event_data):
#   product_id = event_data['product_id']
#   stock = event_data['stock']
#   quantity = event_data['quantity']
#   new_stock = stock-quantity

#   if new_stock == 0:
#     await update_product_status(product_id)
   
# HANDLERS = [
#     handle_stock_update,   
#     handle_product_status   
# ]


# for message in subscriber.subscribe(subscription_path,callback=callback):
#   event_data = json.loads(message.data.decode('utf-8'))
#   print(f'イベント受信:{event_data}')
#   async def run_handlers():
#     tasks=[handler(event_data) for handler in HANDLERS]
#     await asyncio.gather(*tasks)
  
#   asyncio.run(run_handlers())

#google/pubsub
def callback(message):
  event_data = json.loads(message.data.decode('utf-8'))
  product_id = event_data['product_id']
  stock = event_data['stock']
  quantity = event_data['quantity']
  print(f'イベント受信:{event_data}')

  new_stock = stock-quantity

  async def process():
    await update_stock(product_id,new_stock)
    if new_stock==0:
      await update_product_status(product_id)

  asyncio.run(process())
  message.ack()

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id,subscription_id)
streaming_pull_future = subscriber.subscribe(subscription_path,callback=callback)
print(f'イベント購読開始：order_confirmed')

try:
   streaming_pull_future.result()
except KeyboardInterrupt:
   streaming_pull_future.cancell()
