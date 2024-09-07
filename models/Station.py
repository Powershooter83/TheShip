from models.Vector2 import Vector2


class Station:
    def __init__(self, name, vector2):
        self.name = name
        self.vector2 = vector2

#RESOURCES
GOLD_STONE = Station("Gold Stone", Vector2(-10200, 20500.0))


#COLONIES
ARCHITECT_COLONY = Station("Architect Colony", Vector2(0, 0))

#STATIONS
ARAK_STATION = Station("Arak Station", Vector2(2712, -4044.0))
AZURA_STATION = Station("Azura Station", Vector2(-1000, 1000))
CORE_STATION = Station("Core Station", Vector2(0, 0))
TWENTY_ONE_B_STATION = Station("21-B", Vector2(-17375, -6278.0))
VESTA_STATION = Station("Vesta Station", Vector2(10000, 10000))
ZURRO_STATION = Station("Zurro Station", Vector2(5608.0, 9386.0))