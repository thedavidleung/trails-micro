import pika
import json

def get_park(park_address):
    park_name_dict = {"address" : park_address}

# Connect to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='addresses')

    channel.basic_publish(exchange='', routing_key='addresses', body=json.dumps(park_name_dict))
    print(f' sending {park_name_dict}')

    connection.close()
