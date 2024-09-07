import json
from time import sleep
from typing import List

import requests

from models.Environment import BASE_URL_STORAGE
from models.Item import ItemContainer, Item


def move_first_row(vertical_size: int):
    response = requests.get(f"{BASE_URL_STORAGE}structure")

    data = response.json().get("hold")
    row = data[0]

    for x_position, item in enumerate(row):
        if item is not None:
            items_in_column = __find_items_in_column(data, x_position, vertical_size)
            if items_in_column == 0:
                continue
            __move_item_down(x_position, items_in_column)
            break


def __move_item_down(x_position, items_in_column):
    y_position = 0
    for y in range(items_in_column):
        out_data = {
            "a": {"x": x_position, "y": y_position},
            "b": {"x": x_position, "y": y_position + 1}
        }
        y_position += 1
        requests.post(f"{BASE_URL_STORAGE}swap_adjacent", json=out_data).json()
        sleep(.3)


def __find_items_in_column(data, column_index, vertical_size) -> int:
    items_in_column = vertical_size

    for row_index, row in reversed(list(enumerate(data))):
        item = row[column_index]
        if item is not None and items_in_column != 0:
            items_in_column -= 1
        else:
            break

    return items_in_column


def get_storage_size() -> tuple:
    response = requests.get(f"{BASE_URL_STORAGE}structure")
    structure = json.loads(response.text).get('hold')
    return len(structure) - 1, len(structure[0]) - 1


def get_items() -> List[ItemContainer]:
    response = requests.get(f"{BASE_URL_STORAGE}hold")
    data = json.loads(response.text)
    return __map_to_item_containers(data.get('hold').get('resources'))


def get_hold_free() -> int:
    response = requests.get(f"{BASE_URL_STORAGE}hold")
    data = json.loads(response.text)
    return data.get('hold').get('hold_free')


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
