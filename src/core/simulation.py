from src.configs.grid_config import GridConfig
from src.entities.hideout import Hideout
from src.entities.hunter import Hunter
from src.entities.knight import Knight
from src.entities.treasure import Treasure
import random

from src.enums.treasure_type import TreasureType


class Simulation:
    def __init__(self, size):
        self.size = size
        self.treasures = []
        self.hunters = []
        self.hideouts = []
        self.knights = []

    def populate(self):
        for _ in range(10):
            self.treasures.append(Treasure(random.randint(0, GridConfig.GRID_SIZE - 1), random.randint(0, GridConfig.GRID_SIZE-1), random.choice(list(TreasureType))))
        for _ in range(3):
            hideout = Hideout(random.randint(0, GridConfig.GRID_SIZE-1), random.randint(0, GridConfig.GRID_SIZE-1))
            self.hideouts.append(hideout)
            for _ in range(2):
                hunter = Hunter(hideout.x, hideout.y)
                self.hunters.append(hunter)
                hideout.hunters.append(hunter)
        for _ in range(2):
            self.knights.append(Knight(random.randint(0, GridConfig.GRID_SIZE-1), random.randint(0, GridConfig.GRID_SIZE-1)))

    def step(self):
        for treasure in self.treasures[:]:
            if not treasure.decay():
                self.treasures.remove(treasure)
        for hunter in self.hunters:
            hunter.act(self)
        for knight in self.knights:
            knight.act(self)

    def get_treasure_at(self, x, y):
        for treasure in self.treasures:
            if treasure.x == x and treasure.y == y:
                return treasure
        return None

    def is_simulation_over(self):
        no_treasure = not self.treasures
        all_hunters_gone = not self.hunters
        no_recruit_possible = all(len(hideout.hunters) >= 5 for hideout in self.hideouts)
        return no_treasure or (all_hunters_gone and no_recruit_possible)