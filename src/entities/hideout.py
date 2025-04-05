from src.entities.base_entity import BaseEntity
from src.entities.hunter import Hunter


class Hideout(BaseEntity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.hunters = []
        self.stored_treasure = []

    def recruit(self, world):
        if len(self.hunters) < 5 and self.stored_treasure:
            self.stored_treasure.pop()
            new_hunter = Hunter(self.x, self.y)
            self.hunters.append(new_hunter)
            world.hunters.append(new_hunter)
