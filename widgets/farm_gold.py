import threading
from time import sleep
from models.Station import GOLD_STONE, CORE_STATION
from modules.EasySteeringHandler import steer_to_station
from modules.LaserHandler import aim_laser, activate_laser
from modules.ScannerHandler import wait_for_station_and_total_stop, wait_for_station
from modules.ShopHandler import sell_item
from modules.StorageHandler import move_lowest_item_to_lowest_position, get_hold_free, get_items


def move_item_thread():
    while True:
        if get_hold_free() > 0:
            move_lowest_item_to_lowest_position()


def start():
    steer_to_station(GOLD_STONE)
    wait_for_station_and_total_stop(GOLD_STONE)
    aim_laser()

    # Multi Thread to avoid delays
    item_thread = threading.Thread(target=move_item_thread, daemon=True)
    item_thread.start()

    while get_hold_free() != 0:
        activate_laser()
        sleep(10)

    steer_to_station(CORE_STATION)
    wait_for_station(CORE_STATION)

    while len(get_items()) != 0:
        for item_container in get_items():
            sell_item(CORE_STATION, item_container)
        sleep(1)
    start()


start()
