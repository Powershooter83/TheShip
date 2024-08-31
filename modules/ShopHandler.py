import requests

from models.Environment import BASE_URL, BASE_URL_STORAGE, BASE_URL_STORE
from models.Station import Station
from models.Item import Item, ItemContainer


def buy_item(station: Station, item_container: ItemContainer):
    data = {"station": station.name, "what": item_container.item.name, "amount": item_container.amount}
    try:
        response = requests.post(f"{BASE_URL_STORE}buy", json=data)
        print('LOGGER: ' + response.text)
        return response.status_code, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)


def sell_item(station: Station, item_container: ItemContainer):
    data = {"station": station.name, "what": item_container.item.name, "amount": item_container.amount}
    print(data)
    try:
        response = requests.post(f"{BASE_URL_STORE}sell", json=data)
        return response.status_code, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)
