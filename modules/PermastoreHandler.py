import requests

from models.Environment import BASE_URL_PERMASTORE
from models.Station import Station, ZURRO_STATION, AZURA_STATION


def download_to_permastore(from_destination: Station, to_destination: Station):
    try:
        data = {"source": from_destination.name,
                "destination": to_destination.name
                }

        return requests.post(f"{BASE_URL_PERMASTORE}download", json=data)
    except requests.exceptions.RequestException as e:
        raise e


print(download_to_permastore(ZURRO_STATION, AZURA_STATION).text)
