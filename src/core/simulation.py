from src.configs.grid_config import GridConfig
from src.entities.hideout import Hideout
from src.entities.hunter import Hunter # Standard Hunter
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
        self.garrison_locations = GridConfig.GARRISON_LOCATIONS
        self.simulation_step = 0

    def populate(self):
        for _ in range(10):
            self.treasures.append(Treasure(random.randint(0, GridConfig.GRID_SIZE - 1),
                                          random.randint(0, GridConfig.GRID_SIZE-1),
                                          random.choice(list(TreasureType))))
        for _ in range(3):
            self.knights.append(Knight(random.randint(0, GridConfig.GRID_SIZE-1),
                                      random.randint(0, GridConfig.GRID_SIZE-1)))

        for _ in range(3):
            hideout = Hideout(random.randint(0, GridConfig.GRID_SIZE-1),
                              random.randint(0, GridConfig.GRID_SIZE-1))
            self.hideouts.append(hideout)
            num_initial_hunters = random.randint(1, 2)
            for _ in range(num_initial_hunters):
                hunter = Hunter(hideout.x, hideout.y)
                self.hunters.append(hunter)
                hideout.associated_hunters.append(hunter)


    def step(self):
        self.simulation_step += 1

        self.treasures[:] = [t for t in self.treasures if t.decay()]

        for hunter in self.hunters:
             if not hunter.is_dead:
                 hunter.act(self)

        for knight in self.knights:
            knight.act(self)

        for hideout in self.hideouts:
            hideout.recruit(self)

        original_hunter_count = len(self.hunters)
        self.hunters[:] = [h for h in self.hunters if not h.is_dead]

        if len(self.hunters) != original_hunter_count:
             for hideout in self.hideouts:
                 hideout.update_associated_hunters(self.hunters)

    def get_treasure_at(self, x, y):
        for treasure in self.treasures:
            if treasure.x == x and treasure.y == y:
                return treasure
        return None

    def is_simulation_over(self):
        no_treasure = not self.treasures

        recruitment_possible = False

        if self.hunters:
             recruitment_possible = any(len(h.associated_hunters) < Hideout.MAX_HUNTERS for h in self.hideouts)

        simulation_over = no_treasure or (not self.hunters and not recruitment_possible)
        return simulation_over