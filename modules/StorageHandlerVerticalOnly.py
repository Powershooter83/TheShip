from time import sleep

import requests

from models.Environment import BASE_URL_STORAGE
from models.Vector2 import Vector2


def move_first_row(range_vertical: int):
    response = requests.get(f"{BASE_URL_STORAGE}structure")

    data = response.json().get("hold")

    row = data[0]
    for x in range(12):
        if row[x] is not None:
            __move_item_down(Vector2(x, 0), range_vertical)


def __move_item_down(position: Vector2, range_vertical: int):
    for y in range(range_vertical):
        out_data = {
            "a": {"x": position.x, "y": position.y},
            "b": {"x": position.x, "y": position.y + 1}
        }
        position.y += 1
        requests.post(f"{BASE_URL_STORAGE}swap_adjacent", json=out_data).json()
        sleep(.5)