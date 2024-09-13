import base64
import json
import socket
import struct
import sys
from xmlrpc.client import SafeTransport

import websockets
import xmlrpc.client

import requests
from quart import Quart, request

from models.Station import StationEnum, Station

app = Quart(__name__)


def __find_station_by_name(station_name):
    for station in StationEnum:
        if station.value.name == station_name:
            return station


def __azura_interface_send(station: Station, msg):
    base64_encoded = base64.b64encode(bytearray(msg))
    base64_string = base64_encoded.decode('utf-8')

    data = {"sending_station": station.name, "base64data": base64_string}
    requests.post(f"{StationEnum.AZURA.value.get_url()}put_message", json=data)

def __core_interface_send(station: Station, msg):
    base64_encoded = base64.b64encode(bytearray(msg))
    base64_string = base64_encoded.decode('utf-8')

    data = {"source": station.name, "message": base64_string}
    requests.post(f"{StationEnum.CORE.value.get_url()}send", json=data)

def __azura_interface_receive(destination_station: Station):
    received_messages = json.loads(requests.get(f"{StationEnum.AZURA.value.get_url()}messages_for_other_stations").text).get(
        "received_messages")
    messages = []
    for message in received_messages:
        dest = message.get("dest")

        if dest == destination_station.name:
            msg = message.get("base64data")
            decoded_bytes = base64.b64decode(msg)
            messages.append({"destination": destination_station.name, "data": list(decoded_bytes)})
    return {"kind": "success", "messages": messages}


def __zurro_interface_receive(destination_station: Station):
    received_messages = json.loads(requests.post(f"{StationEnum.ZURRO.value.get_url()}receive").text).get(
        "received_messages")
    messages = []
    for message in received_messages:
        dest = message.get("dest")

        if dest == destination_station.name:
            msg = message.get("msg")
            decoded_bytes = base64.b64decode(msg)
            messages.append({"destination": destination_station.name, "data": list(decoded_bytes)})
    return {"kind": "success", "messages": messages}


def __aurora_interface_receive(destination_station: Station):
    server_ip = '192.168.100.21'
    server_port = 2031

    # Verbindung zum Server herstellen
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((server_ip, server_port))

        # Beispielnachricht vorbereiten (src_dst und src_or_dst Werte anpassen)
        src_dst = 1  # Beispielwert für src/dst (1 Byte)
        src_or_dst = destination_station.name  # Zielquelle oder -adresse (UTF-8)
        msg = b'Test message'  # Beispielnachricht (Byte-Array)

        # Größe der Nachricht berechnen
        msg_size = len(src_or_dst) + len(msg)

        # Nachricht zusammenbauen
        message = struct.pack('>H', msg_size)  # Größe der Nachricht (2 Bytes, big endian)
        message += struct.pack('>B', src_dst)  # Quelle/Ziel (1 Byte)
        message += src_or_dst.encode('utf-8')  # Quelle oder Ziel (UTF-8)
        message += msg  # Nachricht (Byte-Array)

        # Nachricht senden
        sock.sendall(message)

        # Empfang der vollständigen Antwort
        data = b''
        while True:
            chunk = sock.recv(4096)  # Puffergröße von 4096 Bytes
            if not chunk:
                break
            data += chunk

            if len(data) >= 3:  # Mindestens 3 Bytes (size of msg, src/dst)
                msg_size = struct.unpack('>H', data[:2])[0]
                if len(data) >= 3 + msg_size:
                    break

        # Nachricht zerlegen
        if len(data) >= 3:
            msg_size = struct.unpack('>H', data[:2])[0]
            src_dst = struct.unpack('>B', data[2:3])[0]
            src_or_dst_len = len(data[3:]) - msg_size
            src_or_dst = data[3:3 + src_or_dst_len].decode('utf-8')
            response_msg = data[3 + src_or_dst_len:]

            print(f"Received data from {src_or_dst} ({src_dst}): {response_msg}", file=sys.stdout)
        else:
            print("Received incomplete or invalid data.", file=sys.stdout)

def __core_interface_receive(destination_station: Station):
    received_messages = json.loads(requests.post(f"{StationEnum.CORE.value.get_url()}receive").text).get(
        "received_messages")
    messages = []
    for message in received_messages:
        dest = message.get("target")

        if dest == destination_station.name:
            msg = message.get("data")
            decoded_bytes = base64.b64decode(msg)
            messages.append({"destination": destination_station.name, "data": list(decoded_bytes)})
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
            json_string = json.dumps(json.loads(data.decode('utf-8')))
            json_bytes = json_string.encode('utf-8')
            json_bytearray = bytearray(json_bytes)
            messages.append({"destination": destination_station.name, "data": list(json_bytearray)})
    return {"kind": "success", "messages": messages}


async def __elyse_interface_receive(destination_station):
    server_url = "ws://192.168.100.21:2026/api"
    messages = []

    async with websockets.connect(server_url) as websocket:
        message = await websocket.recv()

        while True:
            response_data = json.loads(message)
            if response_data.get("destination") == destination_station.name:
                messages.append({"destination": destination_station.name, "data": list(response_data.get('msg'))})
                break

    return {"kind": "success", "messages": messages}


@app.route('/<dest_station_name>/send', methods=['POST'])
async def send(dest_station_name):
    dest_station = __find_station_by_name(dest_station_name)
    data = await request.get_json(force=True)
    source_station = __find_station_by_name(data['source'])
    match dest_station:
        case StationEnum.AZURA:
            __azura_interface_send(source_station.value, data['data'])
        case StationEnum.CORE:
            __core_interface_send(source_station.value, data['data'])
    return {"kind": "success"}


@app.route('/<source_station_name>/receive', methods=['POST'])
async def receive(source_station_name):
    source_station = __find_station_by_name(source_station_name)
    match source_station:

        case StationEnum.ZURRO:
            return __zurro_interface_receive(StationEnum.AZURA.value)
        case StationEnum.ARTEMIS:
            return __artemis_interface_receive(StationEnum.AZURA.value)
        case StationEnum.ELYSE_TERMINAL:
            return await __elyse_interface_receive(StationEnum.AZURA.value)
        case StationEnum.CORE:
            return __core_interface_receive(StationEnum.AZURA.value)
        case StationEnum.AZURA:
            return __azura_interface_receive(StationEnum.CORE.value)
        case StationEnum.AURORA:
            return __aurora_interface_receive(StationEnum.AURORA.value)
    return {"kind": "success"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2023, debug=True)
