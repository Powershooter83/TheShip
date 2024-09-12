from models.Item import Item
from models.Station import StationEnum, ResourceEnum
from modules.FarmManager import FarmManager


gold_farm = FarmManager(StationEnum.CORE.value, ResourceEnum.GOLD.value, Item.GOLD, True)
gold_farm.start()