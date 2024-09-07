from models.Item import Item
from models.Station import CORE_STATION, GOLD_STONE
from modules.FarmManager import FarmManager


gold_farm = FarmManager(CORE_STATION, GOLD_STONE, Item.GOLD, True)
gold_farm.start()