import random

from src.configs.grid_config import GridConfig
from src.entities.base_entity import BaseEntity


class Hunter(BaseEntity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.stamina = 100
        self.carrying = None

    def act(self, world):
        self.stamina -= 2
        if self.stamina <= 0:
            return

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                tx, ty = (self.x + dx) % GridConfig.GRID_SIZE, (self.y + dy) % GridConfig.GRID_SIZE
                treasure = world.get_treasure_at(tx, ty)
                if treasure:
                    self.carrying = treasure
                    world.treasures.remove(treasure)
                    return

        self.move(random.choice([-1, 0, 1]), random.choice([-1, 0, 1]))