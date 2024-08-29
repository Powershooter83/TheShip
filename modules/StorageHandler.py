from time import sleep

import requests

from models.Environment import BASE_URL_STORAGE
from models.Vector2 import Vector2

used_positions = []
def find_lowest_item():
    response = requests.get(f"{BASE_URL_STORAGE}structure")
    for y in reversed(range(10)):
        data = response.json().get("hold")[y]
        for x in reversed(range(12)):
            if data[x] is not None:
                if Vector2(x, y) in used_positions:
                    continue
                return Vector2(x, y)

def find_lowest_position():
    response = requests.get(f"{BASE_URL_STORAGE}structure")
    for n in reversed(range(10)):
        data = response.json().get("hold")[n]
        for j in reversed(range(12)):
            if data[j] is None:
                return Vector2(j, n)
            else:
                if Vector2(j, n) not in used_positions:
                    used_positions.append(Vector2(j, n))


def move_lowest_item_to_lowest_position():
    position = find_lowest_position()
    lowest_item = find_lowest_item()

    if lowest_item.x > position.x:
        while lowest_item.x > position.x:
            out_data = {
                "a": {"x": lowest_item.x, "y": lowest_item.y},
                "b": {"x": lowest_item.x - 1, "y": lowest_item.y}
            }
            lowest_item.x = lowest_item.x - 1
            print(requests.post(f"{BASE_URL_STORAGE}swap_adjacent", json=out_data).json())
            sleep(1)
    elif lowest_item.x < position.x:
        while lowest_item.x < position.x:
            out_data = {
                "a": {"x": lowest_item.x, "y": lowest_item.y},
                "b": {"x": lowest_item.x + 1, "y": lowest_item.y}
            }
            lowest_item.x = lowest_item.x + 1
            print(requests.post(f"{BASE_URL_STORAGE}swap_adjacent", json=out_data).json())
            sleep(1)

    while lowest_item.y < position.y:
        out_data = {
            "a": {"x": lowest_item.x, "y": lowest_item.y},
            "b": {"x": lowest_item.x, "y": lowest_item.y + 1}
        }
        lowest_item.y = lowest_item.y + 1
        print(requests.post(f"{BASE_URL_STORAGE}swap_adjacent", json=out_data).json())
        sleep(1)

for j in range(100):
    move_lowest_item_to_lowest_position()