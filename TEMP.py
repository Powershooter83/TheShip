from time import sleep

from models.EnergyComponent import EnergyComponent, EnergyComponentEnum
from models.Station import StationEnum, ResourceEnum
from models.Vector2 import Vector2
from modules.EasySteeringHandler import steer_to_coordinates, steer_to_station
from modules.EnergyHandler import set_energy
from modules.LaserHandler import aim_laser, activate_laser
from modules.ScannerHandler import wait_for_station_and_total_stop, \
    wait_for_station
from modules.ShopHandler import sell_item
from modules.StorageHandler import get_items

#follow_spaceship("Captain Morris", Vector2(-11000, -11000))

#set_all_components_to_value(0)
#set_energy(EnergyComponent(EnergyComponentEnum.SENSOR_VOID_ENERGY, 100))
#set_energy(EnergyComponent(EnergyComponentEnum.SENSOR_ATOMIC_FIELD, 100))
#set_energy(EnergyComponent(EnergyComponentEnum.SHIELD_GENERATOR, 100))
#set_energy(EnergyComponent(EnergyComponentEnum.MATTER_STABILIZER, 100))

set_energy(EnergyComponent(EnergyComponentEnum.CARGO_BOT, 0))

while(True):
    steer_to_station(StationEnum.CORE.value)
    wait_for_station(StationEnum.CORE.value)
    while len(get_items()) != 0:
        for item_container in get_items():
            sell_item(StationEnum.CORE.value, item_container)
        sleep(1)
    steer_to_coordinates(Vector2(-40300, -51638))
    wait_for_station_and_total_stop(ResourceEnum.MAGNON.value)
    activate_laser()
    aim_laser()
    sleep(3)
    activate_laser()
    sleep(5)
