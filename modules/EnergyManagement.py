import requests

from models.Environment import BASE_URL_E_MANAGEMENT


def change_energy(energyComponentList):
    try:
        data = {}
        for energyComponent in energyComponentList:
            data[energyComponent.component] = energyComponent.limit
        response = requests.put(f"{BASE_URL_E_MANAGEMENT}limit", json=data)
        return response.status_code
    except requests.exceptions.RequestException as e:
        return None, str(e)