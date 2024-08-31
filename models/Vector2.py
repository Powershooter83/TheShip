class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Vector2):
            return self.x == other.x and self.y == other.y
        return False

    def equals_as_integers(self, other):
        if isinstance(other, Vector2):
            return int(self.x) == int(other.x) and int(self.y) == int(other.y)
        return False

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"Vector2(x={self.x}, y={self.y})"