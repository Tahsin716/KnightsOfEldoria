from src.entities.base_entity import BaseEntity

class Treasure(BaseEntity):
    def __init__(self, x, y, t_type):
        super().__init__(x, y)
        self.t_type = t_type
        self.value = float(t_type.value)

    def decay(self):
        if self.value > 0:
            decay_amount = self.value * 0.001
            self.value -= decay_amount

            if self.value <= 0:
                 self.value = 0

        return self.value > 0

    def __repr__(self):
        return f"Treasure({self.t_type.name}, val={self.value:.2f} at ({self.x},{self.y}))"