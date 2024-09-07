from models.Item import Item
from models.Station import CORE_STATION, VESTA_STATION
from modules.FarmManager import FarmManager


iron_farm = FarmManager(CORE_STATION, VESTA_STATION, Item.IRON, False)
iron_farm.start()