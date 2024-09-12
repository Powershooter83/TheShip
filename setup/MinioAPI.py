import base64
import json
import sys

import requests
from flask import Flask, request

from models.Station import StationEnum, Station

app = Flask(__name__)

def __find_station_by_name(station_name):
    for station in StationEnum:
        if station.value.name == station_name:
            return station


def __zurro_interface_send(station: StationEnum, msg):
    try:
        decoded_bytes = base64.b64decode(msg)
        decoded_str = decoded_bytes.decode('utf-8')

        data = {"src": station.value.name, "msg": decoded_str}
        return requests.post(f"{StationEnum.ZURRO.value.get_url()}send", json=data)
    except requests.exceptions.RequestException as e:
        raise e

def __zurro_interface_receive(destination_station: Station):
    received_messages = json.loads(requests.post(f"{StationEnum.ZURRO.value.get_url()}receive").text).get("received_messages")
    messages = []
    print(received_messages)
    for message in received_messages:
        dest = message.get("dest")
        print(dest, file=sys.stdout)
        print(destination_station.name, file=sys.stdout)
        if dest == destination_station.name:
            print("DESTINATION", file=sys.stdout)
            print(dest, file=sys.stdout)
            msg = message.get("msg")
            decoded_bytes = base64.b64decode(msg)
            decoded_str = decoded_bytes.decode('utf-8')
            messages.append({"destination": destination_station.name, "data": decoded_str})
    return {"kind": "success", "messages": messages}


@app.route('/<station_name>/send', methods=['POST'])
def send(station_name):
    station = __find_station_by_name(station_name)
    data = request.json
    source_station = __find_station_by_name(data['source'])
    match station:
        case StationEnum.ZURRO:
            return __zurro_interface_send(source_station, data['data'])


@app.route('/<dest_station_name>/receive', methods=['POST'])
def receive(dest_station_name):
    print(dest_station_name,  file=sys.stdout)
    destination_station = __find_station_by_name(dest_station_name)
    match destination_station:
        case StationEnum.ZURRO:
            return __zurro_interface_receive(destination_station.value)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2023, debug=True)
