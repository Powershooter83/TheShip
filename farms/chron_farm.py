from models.Item import Item
from models.Station import StationEnum, Station
from models.Vector2 import Vector2
from modules.FarmManager import FarmManager


chron_farm = FarmManager(StationEnum.CORE.value,
                        Station("Fragilon Rock", Vector2(44800, -53911), None),
                          Item.FRAGILON, True)
chron_farm.start()