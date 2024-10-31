import threading
from time import sleep

from models.Item import ItemContainer, Item
from models.Station import Station, StationEnum
from modules.EasySteeringHandler import steer_to_station
from modules.LaserHandler import aim_laser, activate_laser
from modules.ScannerHandler import wait_for_station_and_total_stop, wait_for_station
from modules.ShopHandler import sell_item, buy_item
from modules.StorageHandler import move_first_row, get_hold_free, get_storage_size, get_items

stop_event = threading.Event()


def start_laser_thread():
    while not stop_event.is_set():
        print(activate_laser())
        for _ in range(10):
            if stop_event.is_set():
                break
            sleep(1)


def start_buy_item_thread(buy_station: Station, item_container: ItemContainer):
    while True:
        if stop_event.is_set():
            break
        buy_item(buy_station, item_container)
        sleep(2)


class FarmManager:
    def __init__(self, sell_station: Station, buy_station: Station, item_type: Item, laser: bool):
        self.sell_station = sell_station
        self.buy_station = buy_station
        self.item_type = item_type
        self.thread = None
        self.laser = laser

    def start(self):
        laser_thread = None
        buy_thread = None
        print("TOTAL_STOP-1")
        print(self.buy_station.name)
        steer_to_station(self.buy_station)
        wait_for_station_and_total_stop(self.buy_station)
        print("TOTAL_STOP")
        if self.laser:
            aim_laser()
            laser_thread = threading.Thread(target=start_laser_thread)
            laser_thread.start()
        else:
            buy_thread = threading.Thread(target=start_buy_item_thread,
                                          args=(self.buy_station, ItemContainer(self.item_type, get_hold_free())))
            buy_thread.start()

        vertical_size, horizontal_size = get_storage_size()
        while True:
            if get_hold_free() > 0:
                move_first_row(vertical_size)
            else:
                stop_event.set()
                if self.laser:
                    laser_thread.join()
                else:
                    buy_thread.join()
                break

        steer_to_station(self.sell_station)
        wait_for_station(self.sell_station)

        while len(get_items()) != 0:
            for item_container in get_items():
                sell_item(self.sell_station, item_container)
            sleep(1)
        stop_event.clear()
        self.start()
