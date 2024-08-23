import requests

from models.Environment import BASE_URL
from models.Station import Station


def easy_steering(station: Station):
    data = {"target": station}
    try:
        response = requests.post(f"{BASE_URL}set_target", json=data)
        return response.status_code, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)
