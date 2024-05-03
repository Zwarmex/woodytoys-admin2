from flask import Flask, request
import redis
import woody
from datetime import datetime

app = Flask('misc_service')
redis_db = redis.Redis(host='redis', port=6379, db=0)

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
    redis_db.setex(cache_key, 60, result_with_time)  # Cache the value with an expiration of 60 seconds
    return result_with_time

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002)

