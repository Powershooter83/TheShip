import requests

from models.Environment import BASE_URL_PERMASTORE
from models.Station import Station


def download_to_permastore(from_destination: Station, to_destination: Station):
    data = {"source": "Elyse Terminal",
            "destination": "Artemis Station"}

    return requests.post(f"{BASE_URL_PERMASTORE}download", json=data)


def download_to_permastore12():
    return requests.post("http://192.168.100.21:2019/upload",
                         json={"source": "Zurro Station", "destination": "Azura Station"})


print(download_to_permastore12().text)
