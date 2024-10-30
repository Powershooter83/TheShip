from models.Item import Item
from models.Station import StationEnum, ResourceEnum
from modules.FarmManager import FarmManager


fragilon_farm = FarmManager(StationEnum.CORE.value, ResourceEnum.FRAGILON.value, Item.FRAGILON, True)
fragilon_farm.start()