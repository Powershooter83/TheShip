import json
import threading

from models.Vector2 import Vector2
from modules.EasySteeringHandler import steer_to_coordinates
from modules.ScannerHandler import wait_for_coordinates, wait_for_any_station

unique_stations = []


def wait_for_station():
    while True:
        for station in wait_for_any_station():
            if station not in unique_stations:
                f = open("stations.json", "a")
                f.write(json.dumps(station) + "\n")
                f.close()
                unique_stations.append(station)
                print(station)


def search_colony():
    center_x = 0
    center_y = 0

    deviation = 100000

    start_x = center_x - deviation
    end_x = center_x + deviation
    start_y = center_y - deviation
    end_y = center_y + deviation

    step_size = 3000

    x = start_x
    while x <= end_x:
        steer_to_coordinates(Vector2(x, start_y))
        wait_for_coordinates(Vector2(x, start_y))
        steer_to_coordinates(Vector2(x, end_y))
        wait_for_coordinates(Vector2(x, end_y))

        x += step_size

        if x <= end_x:
            steer_to_coordinates(Vector2(x, end_y))
            wait_for_coordinates(Vector2(x, end_y))
            steer_to_coordinates(Vector2(x, start_y))
            wait_for_coordinates(Vector2(x, start_y))


thread_station = threading.Thread(target=wait_for_station)
thread_station.start()
search_colony()
thread_station.join()
