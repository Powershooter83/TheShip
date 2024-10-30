import json
from asyncio import sleep

import pika
import requests

from models.Environment import BASE_URL, HOST
from models.Station import Station
from models.Vector2 import Vector2


def steer_to_station(station: Station):
    steer_to_coordinates(station.vector2)


def steer_to_coordinates(vector2: Vector2):
    data = {"target": {"x": vector2.x, "y": vector2.y}}
    try:
        response = requests.post(f"{BASE_URL}set_target", json=data)
        return response.status_code, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)


def follow_spaceship(spaceship, location: Vector2):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST, port=2014))
    channel = connection.channel()

    channel.exchange_declare(exchange='scanner/detected_objects', exchange_type='fanout')
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='scanner/detected_objects', queue=queue_name)

    steer_to_coordinates(location)

    for method_frame, properties, body in channel.consume(queue=queue_name, auto_ack=True):
        data = json.loads(body.decode('utf-8'))

        for station in data:
            if station['name'] == spaceship:
                print('steer_to_coordinates!')
                steer_to_coordinates(Vector2(station['pos']['x'], station['pos']['y']))


