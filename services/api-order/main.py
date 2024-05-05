from flask import Flask, request
import redis
import woody
from datetime import datetime
import uuid
import pika
import json

app = Flask('order_service')
redis_db = redis.Redis(host='redis', port=6379, db=0)

# Connexion à RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()

# Déclaration de la file d'attente
channel.queue_declare(queue='order_queue', durable=True)

def callback(ch, method, properties, body):
    order_data = json.loads(body)
    order_id = order_data['order_id']
    product = order_data['product']
    timestamp = order_data['timestamp']

    # Process the order
    process_order(order_id, product)

    print(f"Order {order_id} processed successfully at {timestamp}")

# Définition du consommateur
channel.basic_consume(queue='order_queue', on_message_callback=callback, auto_ack=True)

@app.route('/api/orders/do', methods=['GET'])
def create_order():
    product = request.args.get('product')
    order_id = str(uuid.uuid4())

    # Envoie du message à RabbitMQ
    order_data = {
        'order_id': order_id,
        'product': product,
        'timestamp': str(datetime.now())
    }
    channel.basic_publish(exchange='', routing_key='order_queue', body=json.dumps(order_data), properties=pika.BasicProperties(delivery_mode=2))  # make message persistent

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
    # Démarrer la consommation des messages de la file d'attente
    channel.start_consuming()

    # Démarrer l'application Flask
    app.run(host='0.0.0.0', port=5004)

