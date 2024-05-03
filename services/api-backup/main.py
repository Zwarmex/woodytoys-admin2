import uuid
from datetime import datetime

from flask import Flask, request
from flask_cors import CORS
import redis

import woody

app = Flask('my_api')
cors = CORS(app)

redis_db = redis.Redis(host='redis', port=6379, db=0)

@app.get('/api/ping')
def ping():
    return 'ping'

@app.route('/api/misc/time', methods=['GET'])
def get_time():
    return f'misc: {datetime.now()}'

@app.route('/api/misc/heavy', methods=['GET'])
def get_heavy():
    name = request.args.get('name')
    cache_key = f'heavy_result:{name}'
    cached_result = redis_db.get(cache_key)
    if cached_result:
        return cached_result

    result = woody.make_some_heavy_computation(name)
    result_with_time = f'{datetime.now()}: {result}'
    redis_db.setex(cache_key, 60, result_with_time)  # Cache la valeur avec une expiration de 60 secondes
    return result_with_time

@app.route('/api/products/last', methods=['GET'])
def get_last_product():
    cache_key = 'last_product'
    cached_result = redis_db.get(cache_key)
    if cached_result:
        return cached_result

    last_product = woody.get_last_product()  # note: it's a very slow db query
    result_with_time = f'db: {datetime.now()} - {last_product}'
    redis_db.setex(cache_key, 60, result_with_time)  # Cache la valeur avec une expiration de 60 secondes
    return result_with_time

@app.route('/api/orders/do', methods=['GET'])
def create_order():
    product = request.args.get('product')
    order_id = str(uuid.uuid4())

    # very slow process because some payment validation is slow (maybe make it asynchronous ?)
    process_order(order_id, product)

    return f"Your process {order_id} has been created"

@app.route('/api/orders/', methods=['GET'])
def get_order():
    order_id = request.args.get('order_id')
    status = woody.get_order(order_id)
    return f'order "{order_id}": {status}'

def process_order(order_id, order):
    status = woody.make_heavy_validation(order)
    woody.save_order(order_id, status, order)

if __name__ == "__main__":
    woody.launch_server(app, host='0.0.0.0', port=5000)

