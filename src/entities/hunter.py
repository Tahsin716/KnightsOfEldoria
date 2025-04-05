import random

from src.configs.grid_config import GridConfig
from src.entities.base_entity import BaseEntity


class Hunter(BaseEntity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.stamina = 100
        self.carrying = None

    def act(self, world):
        if self.stamina <= 0:
            return

        self.stamina -= 1

        if self.carrying or self.stamina <= 20:
            nearest_hideout = min(world.hideouts, key=lambda h: abs(h.x - self.x) + abs(h.y - self.y))
            dx = 1 if nearest_hideout.x > self.x else -1 if nearest_hideout.x < self.x else 0
            dy = 1 if nearest_hideout.y > self.y else -1 if nearest_hideout.y < self.y else 0
            self.move(dx, dy)

            if self.x == nearest_hideout.x and self.y == nearest_hideout.y:
                self.stamina = 100
                if self.carrying:
                    nearest_hideout.stored_treasure.append(self.carrying)
                    self.carrying = None
            return

        treasure = world.get_treasure_at(self.x, self.y)
        if treasure:
            self.carrying = treasure
            world.treasures.remove(treasure)
            return

        self.move(random.choice([-1, 0, 1]), random.choice([-1, 0, 1]))
