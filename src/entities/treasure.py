from src.entities.base_entity import BaseEntity


class Treasure(BaseEntity):
    def __init__(self, x, y, t_type):
        super().__init__(x, y)
        self.t_type = t_type
        self.value = t_type.value

    def decay(self):
        self.value -= 0.1
        return self.value > 0