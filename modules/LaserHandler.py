from time import sleep

import requests

from models.Environment import BASE_URL_LASER
from models.LaserState import LaserState


def activate_laser():
    try:
        response = requests.post(f"{BASE_URL_LASER}activate")
        print(response)
        return response.status_code, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)


def deactivate_laser():
    try:
        response = requests.post(f"{BASE_URL_LASER}deactivate")
        return response.status_code, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)


def state_laser():
    try:
        response = requests.get(f"{BASE_URL_LASER}state")

        if response.status_code == 200:
            data = response.json()  # Parse the JSON response
            if data["is_mining"]:
                return LaserState.IS_MINING
            elif data["is_cooling_down"]:
                return LaserState.IS_COOLING_DOWN
            elif data["is_active"]:
                return LaserState.IS_ACTIVE
        else:
            return response.status_code, response.text

    except requests.exceptions.RequestException as e:
        return None, str(e)


def aim_laser():
    angle = 0
    try:
        activate_laser()
        while 1 == 1:
            sleep(1)
            response = requests.put(f"{BASE_URL_LASER}angle", json= {"angle": angle})
            state = state_laser()
            print(state)
            if state == LaserState.IS_MINING:
                break
            angle+=36
        return response.status_code, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)
