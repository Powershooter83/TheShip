import requests

from models.Environment import BASE_URL_STORE
from models.Item import ItemContainer
from models.Station import Station


def __send_request(action: str, station: Station, item_container: ItemContainer) -> tuple:
    data = {
        "station": station.name,
        "what": item_container.item.name,
        "amount": item_container.amount
    }
    try:
        response = requests.post(f"{BASE_URL_STORE}{action}", json=data)
        return response.status_code, response.text
    except requests.exceptions.RequestException as e:
        raise e


def buy_item(station: Station, item_container: ItemContainer):
    return __send_request("buy", station, item_container)


def sell_item(station: Station, item_container: ItemContainer):
    return __send_request("sell", station, item_container)
