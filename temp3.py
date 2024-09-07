import base64
import json

import requests

from models.Station import AZURA_STATION, ZURRO_STATION
from models.Vector2 import Vector2
from modules.EasySteeringHandler import steer_to_coordinates


def zurro_rest():
    try:
        return requests.post(f"{ZURRO_STATION.get_url()}receive")
    except requests.exceptions.RequestException as e:
        raise e


data = {"sending_station": "Azura Station",
        "base64data": "ewogIm1lc3NhZ2UiOiAie1xuIFwic291cmNlXCI6IFwiWnVycm8gU3RhdGlvblwiLFxuIFwiZGVzdGluYXRpb25cIjogXCJBenVyYSBTdGF0aW9uXCIsXG4gXCJkYXRhXCI6IFwiRm9yc2NodW5nc2RhdGVuIChHcnVwcGUgMTkyLjE2OC4xMDAuMjEpXCIsXG4gXCJ0c1wiOiBcIjE5MjE2OTkyXCJcbn1cbiIsCiAic2lnbmF0dXJlIjogIjI4YjkxMDc0ZmQzYmY3NzVmYzIzOGJlMzZlY2QyYzJkMmI3NTJjODcyMGIxYmUxYjI4YWI1YzcyZGMxMmIwZGQiCn0K"}


def azura_rest():
    try:
        return requests.post(f"{AZURA_STATION.get_url()}put_message", json=data)
    except requests.exceptions.RequestException as e:
        raise e


def transform_messages(received_messages):
    transformed_messages = []

    for item in received_messages:
        dest = item["dest"]
        msg = item["msg"]

        decoded_bytes = base64.b64decode(msg)
        decoded_str = decoded_bytes.decode('utf-8')

        transformed_messages.append({
            "destination": dest,
            "data": decoded_str
        })

    return transformed_messages


steer_to_coordinates(Vector2(8235, 2821))
