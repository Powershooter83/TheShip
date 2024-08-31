import json
from time import sleep

import pika
import requests

from models.Environment import HOST, BASE_URL_NAVIGATION
from models.Station import Station
from models.Vector2 import Vector2


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


def wait_for_station_and_total_stop(searched_station: Station):
    wait_for_station(searched_station)
    last_position = get_current_position()

    while True:
        sleep(1)
        current_position = get_current_position()

        if current_position.equals_as_integers(last_position):
            print("Das Raumschiff bewegt sich nicht mehr.")
            return
        else:
            last_position = current_position


def get_current_position() -> Vector2:
    try:
        response = requests.get(f"{BASE_URL_NAVIGATION}pos")
        data = json.loads(response.text).get('pos')
        return Vector2(data.get('x'), data.get('y'))
    except requests.exceptions.RequestException as e:
        raise e
