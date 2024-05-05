import pika
import json
from woody import create_order
from time import sleep

# Connexion à RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Déclaration de la file d'attente
channel.queue_declare(queue='order_queue', durable=True)

def send_data_to_queue(data):
    channel.basic_publish(exchange='', routing_key='order_queue', body=json.dumps(data), properties=pika.BasicProperties(delivery_mode=2))

def create_and_send_order(product):
    # Créer une commande en utilisant la fonction create_order du module woody
    order_id = create_order(product)

    # Créer un message à envoyer à la file d'attente
    message = {
        'order_id': order_id,
        'product': product,
        'timestamp': str(datetime.now())
    }

    # Envoyer les données à la file d'attente
    send_data_to_queue(message)

if __name__ == "__main__":
    while True:
        # Créer une commande et l'envoyer à la file d'attente
        create_and_send_order("Product Example")
        sleep(5)  # Attendre 5 secondes avant de créer une nouvelle commande

