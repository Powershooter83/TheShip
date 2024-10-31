from models.Item import Item
from models.Station import StationEnum, ResourceEnum, Station
from models.Vector2 import Vector2
from modules.FarmManager import FarmManager


platin_farm = FarmManager(StationEnum.CORE.value,
                        Station("Platin Mountain", Vector2(50000, 77457), None),
                          Item.PLATIN, True)
platin_farm.start()