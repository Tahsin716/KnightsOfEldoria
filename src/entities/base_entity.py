from src.configs.grid_config import GridConfig


class BaseEntity:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x = (self.x + dx) % GridConfig.GRID_SIZE
        self.y = (self.y + dy) % GridConfig.GRID_SIZE