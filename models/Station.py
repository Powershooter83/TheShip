from enum import Enum

from models.Environment import URL
from models.Vector2 import Vector2


class Station:
    def __init__(self, name, vector2, port):
        self.name = name
        self.vector2 = vector2
        self.port = port

    def get_url(self):
        return f"{URL}:{self.port}/"


class ColonyEnum(Enum):
    ARCHITECT = Station("Architect Colony", Vector2(0, 0), None)


class ResourceEnum(Enum):
    GOLD = Station("Gold Stone", Vector2(-10200, 20500.0), None)


class StationEnum(Enum):
    ARAK = Station("Arak Station", Vector2(2712, -4044.0), None)
    AZURA = Station("Azura Station", Vector2(-1000, 1000), 2030)
    CORE = Station("Core Station", Vector2(0, 0), None)
    TWENTY_ONE_B = Station("21-B", Vector2(-17375, -6278.0), None)
    VESTA = Station("Vesta Station", Vector2(10000, 10000), None)
    ZURRO = Station("Zurro Station", Vector2(5608.0, 9386.0), 2029)
