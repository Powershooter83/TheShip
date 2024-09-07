import threading
from time import sleep

import requests

from models.Station import ARCHITECT_COLONY, Station
from models.Vector2 import Vector2
from modules.EasySteeringHandler import steer_to_station, steer_to_coordinates
from modules.ScannerHandler import wait_for_station, wait_for_coordinates


def wait_for_station_2():
    while True:
        print(wait_for_station(ARCHITECT_COLONY))
        print("STATION FOUND")
        sleep(5)
def search_colony():
    print('SEARCH')
    center_x = -80000
    center_y = -80000

    deviation = 32000

    # Start- und Endkoordinaten berechnen
    start_x = center_x - deviation
    end_x = center_x + deviation
    start_y = center_y - deviation
    end_y = center_y + deviation

    # Schrittweite festlegen
    step_size = 5000

    # Raster zur Suche abfahren
    x = start_x
    print(start_x)
    while x <= end_x:
        steer_to_coordinates(Vector2(x, start_y))
        wait_for_coordinates(Vector2(x, start_y))
        steer_to_coordinates(Vector2(x, end_y))
        wait_for_coordinates(Vector2(x, end_y))

        # Wechselt zur nächsten Spalte
        x += step_size

        if x <= end_x:
            steer_to_coordinates(Vector2(x, end_y))
            wait_for_coordinates(Vector2(x, end_y))
            steer_to_coordinates(Vector2(x, start_y))
            wait_for_coordinates(Vector2(x, start_y))

thread_station = threading.Thread(target=wait_for_station_2)
thread_station.start()
search_colony()
thread_station.join()