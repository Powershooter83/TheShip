import base64
import json
import sys
import xmlrpc.client

import requests
from flask import Flask, request

from models.Station import StationEnum, Station

app = Flask(__name__)

def __find_station_by_name(station_name):
    for station in StationEnum:
        if station.value.name == station_name:
            return station


def __azura_interface_send(station: Station, msg):
    base64_encoded = base64.b64encode(bytearray(msg))
    base64_string = base64_encoded.decode('utf-8')

    data = {"sending_station": station.name, "base64data": base64_string}
    requests.post(f"{StationEnum.AZURA.value.get_url()}put_message", json=data)

def __zurro_interface_receive(destination_station: Station):
    received_messages = json.loads(requests.post(f"{StationEnum.ZURRO.value.get_url()}receive").text).get("received_messages")
    messages = []
    for message in received_messages:
        dest = message.get("dest")

        if dest == destination_station.name:
            msg = message.get("msg")
            decoded_bytes = base64.b64decode(msg)
            messages.append({"destination": "Azura Station", "data": list(decoded_bytes)})
    return {"kind": "success", "messages": messages}


def __artemis_interface_receive(destination_station: Station):
    server_url = "http://192.168.100.21:2024/RPC2"
    proxy = xmlrpc.client.ServerProxy(server_url)

    response_receive = proxy.receive()

    messages = []
    for destination, data in response_receive:
        if destination == destination_station.name:
            if isinstance(data, xmlrpc.client.Binary):
                data = data.data

            msg = json.loads(data.decode('utf-8')).get('message')
            decoded_bytes = base64.b64decode(msg)
            messages.append({"destination": "Azura Station", "data": list(decoded_bytes)})
    return {"kind": "success", "messages": messages}



@app.route('/<dest_station_name>/send', methods=['POST'])
def send(dest_station_name):
    dest_station = __find_station_by_name(dest_station_name)
    data = request.get_json(force=True)
    source_station = __find_station_by_name(data['source'])
    match dest_station:
        case StationEnum.AZURA:
            __azura_interface_send(source_station.value, data['data'])
    return {"kind": "success"}


@app.route('/<source_station_name>/receive', methods=['POST'])
def receive(source_station_name):
    source_station = __find_station_by_name(source_station_name)
    match source_station:

        case StationEnum.ZURRO:
            return __zurro_interface_receive(StationEnum.AZURA.value)
        case StationEnum.ARTEMIS:
            return __artemis_interface_receive(StationEnum.AZURA.value)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2023, debug=True)
