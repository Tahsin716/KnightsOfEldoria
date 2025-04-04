from src.entities.base_entity import BaseEntity
import random

class Knight(BaseEntity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.energy = 100

    def act(self, world):
        self.energy -= 1
        self.move(random.choice([-1, 0, 1]), random.choice([-1, 0, 1]))