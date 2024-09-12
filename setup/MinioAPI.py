import base64
import io
import json
import uuid

import requests
from flask import Flask, jsonify, request
import boto3

from models.Station import StationEnum

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

@app.route('/<station>/send', methods=['POST'])
def send(station_name):
    station = __find_station_by_name(station_name)
    data = request.json
    source_station = __find_station_by_name(data['source'])
    match station:
        case StationEnum.ZURRO:
            return __zurro_interface_send(source_station, data['data'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2023, debug=True)
