class EnergyComponent:
    def __init__(self, component, limit):
        self.component = component
        self.limit = limit

    def __eq__(self, other):
        if isinstance(other, EnergyComponent):
            return self.component == other.component and self.limit == other.limit
        return False

    def __hash__(self):
        return hash((self.component, self.limit))

    def __repr__(self):
        return f"EnergyComponent(component={self.component}, limit={self.limit})"
