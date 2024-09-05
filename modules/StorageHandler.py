import json
from time import sleep
from typing import List

import requests

from models.Environment import BASE_URL_STORAGE
from models.Item import Item, ItemContainer
from models.Vector2 import Vector2

used_positions = []
def find_lowest_item() -> Vector2:
    response = requests.get(f"{BASE_URL_STORAGE}structure")
    for y in reversed(range(10)):
        data = response.json().get("hold")[y]
        for x in reversed(range(12)):
            if data[x] is not None:
                if Vector2(x, y) in used_positions:
                    continue
                return Vector2(x, y)

def find_lowest_position() -> Vector2:
    response = requests.get(f"{BASE_URL_STORAGE}structure")
    for n in reversed(range(10)):
        data = response.json().get("hold")[n]
        for j in reversed(range(12)):
            if data[j] is None:
                return Vector2(j, n)
            else:
                if Vector2(j, n) not in used_positions:
                    used_positions.append(Vector2(j, n))

def get_hold_free() -> int:
    response = requests.get(f"{BASE_URL_STORAGE}hold")
    data = json.loads(response.text)
    return data.get('hold').get('hold_free')


def get_items() -> List[ItemContainer]:
    response = requests.get(f"{BASE_URL_STORAGE}hold")
    data = json.loads(response.text)
    return __map_to_item_containers(data.get('hold').get('resources'))

def __map_to_item_containers(data: dict) -> List[ItemContainer]:
    containers = []
    for item_name, amount in data.items():
        if amount > 0:
            try:
                item = Item[item_name]
                containers.append(ItemContainer(item, amount))
            except KeyError:
                continue
    return containers

def move_lowest_item_to_lowest_position():
    position = find_lowest_position()
    lowest_item = find_lowest_item()
    if lowest_item is None:
        return

    while lowest_item.x > position.x:
        out_data = {
            "a": {"x": lowest_item.x, "y": lowest_item.y},
            "b": {"x": lowest_item.x - 1, "y": lowest_item.y}
        }
        lowest_item.x = lowest_item.x - 1
        requests.post(f"{BASE_URL_STORAGE}swap_adjacent", json=out_data).json()
        sleep(.3)

    while lowest_item.x < position.x:
        out_data = {
            "a": {"x": lowest_item.x, "y": lowest_item.y},
            "b": {"x": lowest_item.x + 1, "y": lowest_item.y}
        }
        lowest_item.x = lowest_item.x + 1
        requests.post(f"{BASE_URL_STORAGE}swap_adjacent", json=out_data).json()
        sleep(.5)

    while lowest_item.y < position.y:
        out_data = {
            "a": {"x": lowest_item.x, "y": lowest_item.y},
            "b": {"x": lowest_item.x, "y": lowest_item.y + 1}
        }
        lowest_item.y = lowest_item.y + 1
        requests.post(f"{BASE_URL_STORAGE}swap_adjacent", json=out_data).json()
        sleep(.5)