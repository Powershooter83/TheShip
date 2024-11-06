
from models.Vector2 import Vector2
from modules.EasySteeringHandler import steer_to_coordinates
from modules.EnergyHandler import set_all_components_to_value, set_energy, energy_mode_flying

energy_mode_flying()
steer_to_coordinates(Vector2(-91771, 97201))
#steer_to_coordinates(Vector2(0, 0))