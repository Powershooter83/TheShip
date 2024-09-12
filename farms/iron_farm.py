from models.Item import Item
from models.Station import StationEnum
from modules.FarmManager import FarmManager


iron_farm = FarmManager(StationEnum.CORE.value, StationEnum.VESTA.value, Item.IRON, False)
iron_farm.start()