import requests

from models.Environment import BASE_URL
from models.Station import Station
from models.Item import Item


def buy_item(station: Station, item: Item, amount: int):
    data = {"station": station, "what": item, "amount": amount}
    try:
        response = requests.post(f"{BASE_URL}buy", json=data)
        print('LOGGER: ' + response.text)
        return response.status_code, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)


def sell_item(station: Station, item: Item, amount: int):
    data = {"station": station, "what": item, "amount": amount}
    try:
        response = requests.post(f"{BASE_URL}sell", json=data)
        return response.status_code, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)
