from enum import Enum


class Item(Enum):
    STONE = "STONE"
    IRON = "IRON"
    GOLD = "GOLD"
    PLATIN = "PLATIN"
    URAN = "URAN"
    IRIDIUM = "IRIDIUM"
    FRAGILON = "FRAGILON"


class ItemContainer:
    def __init__(self, item: Item, amount: int):
        self.item = item
        self.amount = amount

    def __repr__(self):
        return f"ItemContainer(item={self.item}, amount={self.amount})"
