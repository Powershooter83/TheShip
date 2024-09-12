from time import sleep

from models.Station import StationEnum
from models.Vector2 import Vector2
from modules.EasySteeringHandler import steer_to_coordinates, steer_to_station
from modules.LaserHandler import activate_laser
from modules.ScannerHandler import steer_to_station_live

# steer_to_coordinates(Vector2(50489,77896))
# auftauen(Vector2(50489, 77896))

steer_to_station(StationEnum.ZURRO.value)