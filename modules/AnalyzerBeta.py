import json
from enum import Enum
from time import sleep
from typing import List

import pika
import requests

HOST = "192.168.100.21"
URL = f"http://{HOST}"
BASE_URL = f"{URL}:2009/"
BASE_URL_LASER = f"{URL}:2018/"
BASE_URL_STORAGE = f"{URL}:2012/"
BASE_URL_STORE = f"{URL}:2011/"
BASE_URL_NAVIGATION = f"{URL}:2010/"
BASE_URL_PERMASTORE = f"{URL}:2019/"
BASE_URL_E_MANAGEMENT_NODE1 = f"{URL}:2032/"
BASE_URL_E_MANAGEMENT_NODE2 = f"{URL}:2033/"

class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Vector2):
            return self.x == other.x and self.y == other.y
        return False

    def equals_as_integers(self, other):
        if isinstance(other, Vector2):
            return int(self.x) == int(other.x) and int(self.y) == int(other.y)
        return False

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"Vector2(x={self.x}, y={self.y})"


class LaserState(Enum):
    IS_MINING = "is_mining"
    IS_COOLING_DOWN = "is_cooling_down"
    IS_ACTIVE = "is_active"
    NOT_FOUND = "not_found"


class Station:
    def __init__(self, name, vector2, port):
        self.name = name
        self.vector2 = vector2
        self.port = port

    def get_url(self):
        return f"{URL}:{self.port}/"


class ColonyEnum(Enum):
    ARCHITECT = Station("Architect Colony", Vector2(-48777, -51374), None)


class ResourceEnum(Enum):
    GOLD = Station("Gold Stone", Vector2(-10200, 20500.0), None)
    PLATIN = Station("Platin Mountain", Vector2(50700, 78000), None)
    FRAGILON = Station("Fragilon Rock", Vector2(44200, -53911), None)
    MAGNON = Station("Magnon Rock", Vector2(-40300, -51638), None)
    CHRON = Station("Chron", Vector2(0, 0), None)


class StationEnum(Enum):
    ARAK = Station("Arak Station", Vector2(2712, -4044.0), None)
    AZURA = Station("Azura Station", Vector2(-1000, 1000), 2030)
    CORE = Station("Core Station", Vector2(0, 0), 2027)
    TWENTY_ONE_B = Station("21-B", Vector2(-17375, -6278.0), None)
    VESTA = Station("Vesta Station", Vector2(10000, 10000), None)
    ZURRO = Station("Zurro Station", Vector2(5608.0, 9386.0), 2029)
    Arakrock = Station("Arakrock 2", Vector2(0, 0), None)
    ARTEMIS = Station("Artemis Station", Vector2(0, 0), None)
    ELYSE_TERMINAL = Station("Elyse Terminal", Vector2(0, 0), None)
    AURORA = Station("Aurora Station", Vector2(0, 0), 2031)


class EnergyComponentEnum(Enum):
    THRUSTER_BACK = "thruster_back"
    THRUSTER_FRONT = "thruster_front"
    THRUSTER_FRONT_LEFT = "thruster_front_left"
    THRUSTER_FRONT_RIGHT = "thruster_front_right"
    THRUSTER_BOTTOM_LEFT = "thruster_bottom_left"
    THRUSTER_BOTTOM_RIGHT = "thruster_bottom_right"
    LASER = "laser"
    CARGO_BOT = "cargo_bot"
    SCANNER = "scanner"
    JUMPDRIVE = "jumpdrive"
    SENSOR_ATOMIC_FIELD = "sensor_atomic_field"
    SENSOR_VOID_ENERGY = "sensor_void_energy"
    SHIELD_GENERATOR = "shield_generator"
    ANALYZER_ALPHA = "analyzer_alpha"
    MATTER_STABILIZER = "matter_stabilizer"


class EnergyComponent:
    def __init__(self, component: EnergyComponentEnum, limit: float):
        self.component = component
        self.limit = limit


def set_energy(energy_component: EnergyComponent):
    components = _get_energy_components_from_api()
    for component in components:
        if component.component == energy_component.component:
            component.limit = energy_component.limit
            break
    set_energies(components)


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


def _get_role_node1():
    try:
        response = requests.get(f"{BASE_URL_E_MANAGEMENT_NODE1}status")
        data = response.json()
        return data.get("role")
    except requests.exceptions.RequestException as e:
        return None, str(e)


def steer_to_coordinates(vector2: Vector2):
    data = {"target": {"x": vector2.x, "y": vector2.y}}
    try:
        response = requests.post(f"{BASE_URL}set_target", json=data)
        return response.status_code, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)


def energy_mode_flying():
    set_all_components_to_value(0.0)
    set_energy(EnergyComponent(EnergyComponentEnum.THRUSTER_BACK, 1))
    set_energy(EnergyComponent(EnergyComponentEnum.THRUSTER_FRONT, 1))
    set_energy(EnergyComponent(EnergyComponentEnum.THRUSTER_FRONT_LEFT, 1))
    set_energy(EnergyComponent(EnergyComponentEnum.THRUSTER_FRONT_RIGHT, 1))
    set_energy(EnergyComponent(EnergyComponentEnum.THRUSTER_BOTTOM_LEFT, 1))
    set_energy(EnergyComponent(EnergyComponentEnum.SCANNER, 1))
    set_energy(EnergyComponent(EnergyComponentEnum.THRUSTER_BOTTOM_RIGHT, 1))


def get_current_position() -> Vector2:
    try:
        response = requests.get(f"{BASE_URL_NAVIGATION}pos")
        data = json.loads(response.text).get('pos')
        return Vector2(data.get('x'), data.get('y'))
    except requests.exceptions.RequestException as e:
        raise e


def set_all_components_to_value(value: float):
    energy_component_list: List[EnergyComponent] = [
        EnergyComponent(component, value) for component in EnergyComponentEnum
    ]
    set_energies(energy_component_list)


def __move_item_down(currentLine):
    for x in range(12):
        for y in range(currentLine):
            out_data = {
                "a": {"x": x, "y": y},
                "b": {"x": x, "y": y + 1}
            }
            print(requests.post(f"{BASE_URL_STORAGE}swap_adjacent", json=out_data))
            sleep(0.5)


def wait_for_station(searched_station: Station):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST, port=2014))
    channel = connection.channel()

    channel.exchange_declare(exchange='scanner/detected_objects', exchange_type='fanout')
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='scanner/detected_objects', queue=queue_name)

    for method_frame, properties, body in channel.consume(queue=queue_name, auto_ack=True):
        data = json.loads(body.decode('utf-8'))
        if data and any(station['name'] == searched_station.name for station in data):
            return


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
            angle += 22
        return response.status_code, response.text
    except requests.exceptions.RequestException as e:
        raise e


def activate_laser():
    try:
        response = requests.post(f"{BASE_URL_LASER}activate")
        return response.status_code
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


def wait_for_station_and_total_stop(searched_station: Station):
    wait_for_station(searched_station)
    last_position = get_current_position()

    while True:
        sleep(1)
        current_position = get_current_position()

        if current_position.equals_as_integers(last_position):
            print("Das Raumschiff bewegt sich nicht mehr.")
            return
        else:
            last_position = current_position


def is_first_array_filled():
    response = requests.get("http://192.168.100.21:2012/structure")
    data = response.json()
    if "hold" in data and len(data["hold"]) > 0:
        return all(item is not None for item in data["hold"][0])
    return False



############################################################################################################################################################
# easy sharable
############################################################################################################################################################


energy_mode_flying()
steer_to_coordinates(Vector2(-18700, 12727))
wait_for_station_and_total_stop(ResourceEnum.CHRON.value)
set_energy(EnergyComponent(EnergyComponentEnum.SENSOR_ATOMIC_FIELD, 1))
set_energy(EnergyComponent(EnergyComponentEnum.MATTER_STABILIZER, 1))
set_energy(EnergyComponent(EnergyComponentEnum.LASER, .3))
aim_laser()
for currentLine in range(11):
    set_all_components_to_value(0.0)
    set_energy(EnergyComponent(EnergyComponentEnum.SENSOR_ATOMIC_FIELD, 1))
    set_energy(EnergyComponent(EnergyComponentEnum.MATTER_STABILIZER, 1))
    set_energy(EnergyComponent(EnergyComponentEnum.LASER, .3))

    while True:
        if is_first_array_filled():
            break
        else:
            activate_laser()
            sleep(9)
    set_energy(EnergyComponent(EnergyComponentEnum.LASER, 0))
    set_energy(EnergyComponent(EnergyComponentEnum.CARGO_BOT, 1))


    __move_item_down(10 - currentLine)
set_energy(EnergyComponent(EnergyComponentEnum.THRUSTER_BACK, 1))
set_energy(EnergyComponent(EnergyComponentEnum.THRUSTER_FRONT, 1))
set_energy(EnergyComponent(EnergyComponentEnum.THRUSTER_FRONT_LEFT, 1))
set_energy(EnergyComponent(EnergyComponentEnum.THRUSTER_FRONT_RIGHT, 1))
set_energy(EnergyComponent(EnergyComponentEnum.THRUSTER_BOTTOM_LEFT, 1))
set_energy(EnergyComponent(EnergyComponentEnum.THRUSTER_BOTTOM_RIGHT, 1))
set_energy(EnergyComponent(EnergyComponentEnum.LASER, 0))
set_energy(EnergyComponent(EnergyComponentEnum.CARGO_BOT, 0))
steer_to_coordinates(Vector2(0, 0))