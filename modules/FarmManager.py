import multiprocessing
from time import sleep

from models.Item import ItemContainer, Item
from models.Station import Station
from modules.EasySteeringHandler import steer_to_station
from modules.LaserHandler import aim_laser, activate_laser
from modules.ScannerHandler import wait_for_station_and_total_stop, wait_for_station
from modules.ShopHandler import sell_item, buy_item
from modules.StorageHandler import move_first_row, get_hold_free, get_storage_size, get_items


class FarmManager:
    def __init__(self, sell_station: Station, buy_station: Station, item_type: Item, laser: bool):
        self.sell_station = sell_station
        self.buy_station = buy_station
        self.item_type = item_type
        self.process = None
        self.laser = laser

    def __buy_item_process(self):
        while True:
            buy_item(self.buy_station, ItemContainer(self.item_type, get_hold_free()))
            sleep(2)

    def __laser_process(self):
        while True:
            activate_laser()
            sleep(4)

    def start(self):
        laser_process = None
        buy_process = None
        steer_to_station(self.buy_station)
        wait_for_station_and_total_stop(self.buy_station)
        if self.laser:
            aim_laser()
            laser_process = multiprocessing.Process(target=self.__laser_process)
            laser_process.start()
        else:
            buy_process = multiprocessing.Process(target=self.__buy_item_process)
            buy_process.start()

        vertical_size, horizontal_size = get_storage_size()
        while True:
            if get_hold_free() > 0:
                move_first_row(vertical_size)
            else:
                if self.laser:
                    laser_process.terminate()
                else:
                    buy_process.terminate()
                break

        steer_to_station(self.sell_station)
        wait_for_station(self.sell_station)

        while len(get_items()) != 0:
            for item_container in get_items():
                sell_item(self.sell_station, item_container)
            sleep(1)
        self.start()
