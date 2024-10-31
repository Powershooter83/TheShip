from time import sleep

import requests

from models.EnergyComponent import EnergyComponent, EnergyComponentEnum
from models.Environment import BASE_URL_LASER
from models.LaserState import LaserState
from modules.EnergyHandler import set_energy


def activate_laser():
    set_energy(EnergyComponent(EnergyComponentEnum.LASER, 1))
    try:
        response = requests.post(f"{BASE_URL_LASER}activate")
        return response.status_code
    except requests.exceptions.RequestException as e:
        return None, str(e)


def deactivate_laser():
    set_energy(EnergyComponent(EnergyComponentEnum.LASER, 0))
    try:
        response = requests.post(f"{BASE_URL_LASER}deactivate")
        return response.status_code, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)


def state_laser() -> LaserState:
    try:
        response = requests.get(f"{BASE_URL_LASER}state")

        if response.status_code == 200:
            data = response.json()
            if data["is_mining"]:
                return LaserState.IS_MINING
            elif data["is_cooling_down"]:
                return LaserState.IS_COOLING_DOWN
            elif data["is_active"]:
                return LaserState.IS_ACTIVE
    except requests.exceptions.RequestException as e:
        raise e


def aim_laser():
    angle = 0
    restart_laser = 3
    try:
        while 1 == 1:
            if restart_laser == 3:
                status_code = activate_laser()
                if status_code == 403:
                    print('MAX-REQUEST/MIN REACHED!')
                    print('WAITING 60 SECONDS')
                    sleep(60)
                    activate_laser()
                restart_laser = 0

            sleep(1)
            response = requests.put(f"{BASE_URL_LASER}angle", json={"angle": angle})
            restart_laser += 1
            state = state_laser()
            if state == LaserState.IS_MINING:
                break
            angle += 30
        return response.status_code, response.text
    except requests.exceptions.RequestException as e:
        raise e
