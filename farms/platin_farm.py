from models.Item import Item
from models.Station import StationEnum, ResourceEnum
from modules.FarmManager import FarmManager


platin_farm = FarmManager(StationEnum.CORE.value, ResourceEnum.PLATIN.value, Item.PLATIN, True)
platin_farm.start()