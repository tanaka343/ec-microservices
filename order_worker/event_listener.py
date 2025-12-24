import redis
import json
import requests

redis_client = redis.Redis(host='localhost',port=6379,decode_responses=True)
pubsub = redis_client.pubsub()
pubsub.subscribe("order_confirmed")

print(f'イベント購読開始：order_confirmed')

for message in pubsub.listen():
  if message['type'] == 'message':
    try:
      event_data = json.loads(message['data'])
      product_id = event_data['product_id']
      stock = event_data['stock']
      quantity = event_data['quantity']
      print(f'イベント受信:{event_data}')

      new_stock = stock-quantity
      response = requests.put(
        f"http://localhost:8002/stock/{product_id}",
            json={'stock':new_stock}
        )
      if response.status_code == 200:
        print(f'在庫更新完了：product_id={product_id},new_stock={new_stock}')
      else:
        print(f'在庫更新失敗:{response.text}')

      if new_stock == 0:
        response = requests.put(
          f"http://localhost:8001/products/{product_id}",
            json={'status':False}
        )
        if response.status_code ==200:
          print(f'販売中止：product_id={product_id}')
    except Exception as e:
      print(f'error:{e}')