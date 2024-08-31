from time import sleep

from models.Station import GOLD_STONE, CORE_STATION
from modules.EasySteeringHandler import steer_to_station
from modules.LaserHandler import aim_laser, activate_laser
from modules.ScannerHandler import wait_for_station_and_total_stop
from modules.ShopHandler import sell_item
from modules.StorageHandler import move_lowest_item_to_lowest_position, get_hold_free, get_items


def start():
    steer_to_station(GOLD_STONE)
    wait_for_station_and_total_stop(GOLD_STONE)
    aim_laser()
    while get_hold_free() != 0:
        activate_laser()
        move_lowest_item_to_lowest_position()
        sleep(5)
    steer_to_station(CORE_STATION)
    for item_container in get_items():
        sell_item(CORE_STATION, item_container)
    start()

start()