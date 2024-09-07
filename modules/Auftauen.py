from time import sleep

from models.Vector2 import Vector2
from modules.EasySteeringHandler import steer_to_coordinates
from modules.LaserHandler import activate_laser
from modules.ScannerHandler import wait_for_coordinates


def auftauen(vector: Vector2):
    steer_to_coordinates(vector)
    wait_for_coordinates(vector)
    while True:
        print(activate_laser())
        sleep(4)

auftauen(Vector2(-10468, -15193))