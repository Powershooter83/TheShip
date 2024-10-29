from typing import List

import requests

from models.EnergyComponent import EnergyComponent
from models.EnergyComponentEnum import EnergyComponentEnum
from models.Environment import BASE_URL_E_MANAGEMENT_NODE1, BASE_URL_E_MANAGEMENT_NODE2, BASE_URL


def set_energies(energy_component_list: list[EnergyComponent]):
    try:
        data = {}
        for energyComponent in energy_component_list:
            data[energyComponent.component.value] = energyComponent.limit

        if _get_role_node1() == 'active':
            response = requests.put(f"{BASE_URL_E_MANAGEMENT_NODE1}limits", json=data)
        else:
            response = requests.put(f"{BASE_URL_E_MANAGEMENT_NODE2}limits", json=data)
        return response.status_code
    except requests.exceptions.RequestException as e:
        return None, str(e)

def set_energy(energy_component: EnergyComponent):
    components = _get_energy_components_from_api()
    for component in components:
        if component.component == energy_component.component:
            component.limit = energy_component.limit
            break
    set_energies(components)

def _get_role_node1():
    try:
        response = requests.get(f"{BASE_URL_E_MANAGEMENT_NODE1}status")
        data = response.json()
        return data.get("role")
    except requests.exceptions.RequestException as e:
        return None, str(e)


def set_all_components_to_value(value: float):
    energy_component_list: List[EnergyComponent] = [
        EnergyComponent(component, value) for component in EnergyComponentEnum
    ]
    set_energies(energy_component_list)


def _get_energy_components_from_api() -> List[EnergyComponent]:
    if _get_role_node1() == 'active':
        response = requests.get(f"{BASE_URL_E_MANAGEMENT_NODE1}limits")
    else:
        response = requests.get(f"{BASE_URL_E_MANAGEMENT_NODE2}limits")
    data = response.json()
    energy_components = []

    for component, limit in data.items():
        for enum_member in EnergyComponentEnum:
            if enum_member.value == component:
                energy_components.append(EnergyComponent(enum_member, limit))
                break

    return energy_components