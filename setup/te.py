from time import sleep

from opcua import Client

from models.EnergyComponent import EnergyComponent, EnergyComponentEnum
from models.Environment import BASE_URL_JUMPDRIVE
from models.Vector2 import Vector2
from modules.EnergyHandler import set_all_components_to_value, set_energy
from modules.JumpDriveHandler import jumpdrive
from modules.MeasurementHandler import trigger_measurement_and_store
from modules.ScannerHandler import get_current_position

trigger_measurement_and_store()