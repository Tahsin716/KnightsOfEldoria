from src.entities.base_entity import BaseEntity


class Hideout(BaseEntity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.hunters = []
        self.stored_treasure = []