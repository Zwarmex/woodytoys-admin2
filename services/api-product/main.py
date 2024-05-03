from flask import Flask
import redis
import woody
from datetime import datetime

app = Flask('product_service')
redis_db = redis.Redis(host='redis', port=6379, db=0)

@app.route('/api/products/last', methods=['GET'])
def get_last_product():
    cache_key = 'last_product'
    cached_result = redis_db.get(cache_key)
    if cached_result:
        return cached_result

    last_product = woody.get_last_product()  # note: it's a very slow db query
    result_with_time = f'db: {datetime.now()} - {last_product}'
    redis_db.setex(cache_key, 60, result_with_time)  # Cache the value with an expiration of 60 seconds
    return result_with_time

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5003)

