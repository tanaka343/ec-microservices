import redis
import json
import requests
import aiohttp
import asyncio

redis_client = redis.Redis(host='localhost',port=6379,decode_responses=True)
pubsub = redis_client.pubsub()
pubsub.subscribe("order_confirmed")

print(f'イベント購読開始：order_confirmed')

async def update_stock(product_id :int,new_stock :int):
    async with aiohttp.ClientSession() as session:
        async with session.put(
            f"http://localhost:8002/stock/{product_id}",
            json={'stock':new_stock}
            ) as response:
            if response.status_code == 200:
              print(f'在庫更新完了：product_id={product_id},new_stock={new_stock}')
            else:
              print(f'在庫更新失敗:{response.text}')

    
async def update_product_status(product_id :int):
    async with aiohttp.ClientSession() as session:
        async with session.put(
            f"http://localhost:8001/products/{product_id}",
            json={'status':False}
            ) as response:
            if response.status_code ==200:
                print(f'販売中止：product_id={product_id}')
            else :
                raise Exception(f"販売状況を更新できません:status={response.status}")

async def handle_stock_update(event_data):
  product_id = event_data['product_id']
  stock = event_data['stock']
  quantity = event_data['quantity']
  print(f'イベント受信:{event_data}')

  new_stock = stock-quantity
  await update_stock(product_id,new_stock)
  
async def handle_product_status(event_data):
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
  if message['type'] == 'message':
    event_data = json.loads(message['data'])
    tasks=[handler(event_data) for handler in HANDLERS]
    asyncio.run(asyncio.gather(*tasks))
