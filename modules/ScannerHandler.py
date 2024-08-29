import json

import pika

from models.Environment import HOST
from models.Station import Station


def wait_for_station(searched_station: Station):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST, port=2014))
    channel = connection.channel()

    channel.exchange_declare(exchange='scanner/detected_objects', exchange_type='fanout')
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='scanner/detected_objects', queue=queue_name)

    for method_frame, properties, body in channel.consume(queue=queue_name, auto_ack=True):
        data = json.loads(body.decode('utf-8'))
        if data and any(station['name'] == searched_station.name for station in data):
            return