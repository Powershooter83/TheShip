import requests

from models.Environment import BASE_URL_E_MANAGEMENT_NODE1, BASE_URL_E_MANAGEMENT_NODE2, BASE_URL


def change_energy(energyComponentList):
    try:
        data = {}
        for energyComponent in energyComponentList:
            data[energyComponent.component.value] = energyComponent.limit

        if(get_role_node1() == 'active'):
            response = requests.put(f"{BASE_URL_E_MANAGEMENT_NODE1}limits", json=data)
        else:
            response = requests.put(f"{BASE_URL_E_MANAGEMENT_NODE2}limits", json=data)
        return response.status_code
    except requests.exceptions.RequestException as e:
        return None, str(e)

def get_role_node1():
    try:
        response = requests.get(f"{BASE_URL_E_MANAGEMENT_NODE1}status")
        data = response.json()
        return data.get("role")
    except requests.exceptions.RequestException as e:
        return None, str(e)

def get_role_node2():
    try:
        response = requests.get(f"{BASE_URL_E_MANAGEMENT_NODE2}status")
        data = response.json()
        return data.get("role")
    except requests.exceptions.RequestException as e:
        return None, str(e)