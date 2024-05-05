from flask import Flask, request
import redis
import woody
from datetime import datetime
import uuid

app = Flask('order_service')
redis_db = redis.Redis(host='redis', port=6379, db=0)

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
    app.run(host='0.0.0.0', port=5004)

