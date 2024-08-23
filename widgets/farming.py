import requests

from models.Environment import BASE_URL
from models.Station import Station
from models.Item import Item


AMOUNT = 12
STATION_START = Station.CORE
STATION_END = Station.VESTA


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


def easy_steering(station: Station):
    data = {"target": station}
    try:
        response = requests.post(f"{BASE_URL}set_target", json=data)
        return response.status_code, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)

# for i in range(12):
#    print("Neuer Durchlauf")
#
#    time.sleep(30)
#    print(buy_item())
#    print(easy_steering("Core Station"))
#    time.sleep(30)
#    print(sell_item())
