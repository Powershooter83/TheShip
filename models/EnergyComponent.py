from models.EnergyComponentEnum import EnergyComponentEnum


class EnergyComponent:
    def __init__(self, component: EnergyComponentEnum, limit: float):
        self.component = component
        self.limit = limit
