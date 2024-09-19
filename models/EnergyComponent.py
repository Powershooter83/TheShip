class EnergyComponent:
    def __init__(self, component, limit):
        self.component = component
        self.limit = limit

    def __eq__(self, other):
        if isinstance(other, EnergyComponent):
            return self.component == other.componten and self.limit == other.limit
        return False

    def __hash__(self):
        return hash((self.component, self.limit))

    def __repr__(self):
        return f"EnergyComponent(x={self.component}, y={self.limit})"
