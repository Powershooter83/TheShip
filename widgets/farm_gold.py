import time

from models.Station import GOLD_STONE, ZURRO_STATION
from modules.EasySteeringHandler import steer_to_station
from modules.LaserHandler import aim_laser, activate_laser, deactivate_laser
from modules.ScannerHandler import wait_for_station
from modules.ShopHandler import sell_item
from modules.StorageHandler import check_is_first_row_empty, test2


def start():
    steer_to_station(GOLD_STONE)
    wait_for_station(GOLD_STONE)

    activate_laser()
    aim_laser()
    while check_is_first_row_empty():
        activate_laser()
        time.sleep(10)
    steer_to_station(ZURRO_STATION)
    deactivate_laser()
    wait_for_station(ZURRO_STATION)
    sell()
    start()



def sell():
    for item, count in test2().items():
        print(sell_item(ZURRO_STATION, item, count))


start()