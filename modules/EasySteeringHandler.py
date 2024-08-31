import requests

from models.Environment import BASE_URL
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
