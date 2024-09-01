import threading
from time import sleep

from models.Item import ItemContainer, Item
from models.Station import CORE_STATION, VESTA_STATION
from modules.EasySteeringHandler import steer_to_station
from modules.ScannerHandler import wait_for_station_and_total_stop, wait_for_station
from modules.ShopHandler import sell_item, buy_item
from modules.StorageHandler import move_lowest_item_to_lowest_position, get_hold_free, get_items


def move_item_thread():
    while True:
        if get_hold_free() > 0:
            move_lowest_item_to_lowest_position()


def start():
    steer_to_station(VESTA_STATION)
    wait_for_station_and_total_stop(VESTA_STATION)
    buy_item(VESTA_STATION, ItemContainer(Item.IRON, get_hold_free()))

    # Multi-Threading to avoid delays
    threads = []
    for _ in range(3):
        item_thread = threading.Thread(target=move_item_thread, daemon=True)
        item_thread.start()
        threads.append(item_thread)

    while get_hold_free() != 0:
        buy_item(VESTA_STATION, ItemContainer(Item.IRON, get_hold_free()))
        sleep(15)

    steer_to_station(CORE_STATION)
    wait_for_station(CORE_STATION)

    while len(get_items()) != 0:
        for item_container in get_items():
            sell_item(CORE_STATION, item_container)
        sleep(1)
    start()


start()
