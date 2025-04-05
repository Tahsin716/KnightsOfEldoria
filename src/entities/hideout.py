from src.entities.base_entity import BaseEntity
from src.entities.hunter import Hunter
import random

class Hideout(BaseEntity):
    MAX_HUNTERS = 5

    def __init__(self, x, y):
        super().__init__(x, y)
        self.associated_hunters = []
        self.stored_treasure = []

    def update_associated_hunters(self, world_hunters):
        self.associated_hunters = [h for h in self.associated_hunters if h in world_hunters]


    def recruit(self, world):
        self.update_associated_hunters(world.hunters)

        if len(self.associated_hunters) >= self.MAX_HUNTERS:
            return

        if random.random() < 0.20:
            new_hunter = Hunter(self.x, self.y)
            self.associated_hunters.append(new_hunter)
            world.hunters.append(new_hunter)

    def __repr__(self):
        return f"Hideout(Treas:{len(self.stored_treasure)}, AssocHunt:{len(self.associated_hunters)} at ({self.x},{self.y}))"