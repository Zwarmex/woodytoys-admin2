from flask import Flask
from datetime import datetime
import redis

from utils import get_last_product, launch_server, make_some_heavy_computation

app = Flask('my_api')

# Connexion à Redis
r = redis.Redis(host='redis', port=6379, db=0)

@app.get('/api/ping')
def ping():
    return 'ping'

@app.get('/api/slow_static')
def slow_static():
    # Vérifie si la valeur est déjà en cache
    cached_result = r.get('slow_static_result')
    if cached_result:
        return cached_result

    # Si la valeur n'est pas en cache, effectue l'opération coûteuse et met en cache le résultat
    result = make_some_heavy_computation()
    r.setex('slow_static_result', 60, result)  # Cache la valeur avec une expiration de 60 secondes
    return result

@app.get('/api/slow_dynamic')
def slow_dynamic():
    # Pour cet endpoint dynamique, nous ne pouvons pas utiliser de cache
    result = make_some_heavy_computation()
    return f'{datetime.now()}: {result}'

@app.get('/api/fast')
def fast():
    return f'fast: {datetime.now()}'

@app.post('/api/database')
def products():
    # Cet endpoint est peut-être dynamique, donc nous ne le mettons pas en cache
    return f'db: {datetime.now()} - {get_last_product()}'

if __name__ == "__main__":
    launch_server(app, host='0.0.0.0', port=5000)

