from models.EnergyComponent import EnergyComponent, EnergyComponentEnum
from models.Vector2 import Vector2
from modules.EasySteeringHandler import steer_to_coordinates, follow_spaceship
from modules.EnergyHandler import set_all_components_to_value, set_energy, energy_mode_flying
from modules.ScannerHandler import get_current_position

follow_spaceship("Captain Morris", get_current_position())