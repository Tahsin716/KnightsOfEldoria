import random
from src.configs.grid_config import GridConfig
from src.entities.base_entity import BaseEntity

class Hunter(BaseEntity):
    MAX_STAMINA = 100
    STAMINA_MOVE_COST = 0.02
    RECOVERY_RATE_PERCENT = 0.01
    STAMINA_CRITICAL_LEVEL = 6
    SCAN_RADIUS = 1

    def __init__(self, x, y):
        super().__init__(x, y)
        self.stamina = self.MAX_STAMINA
        self.carrying = None
        self.is_dead = False
        self.is_caught = False

    def _calculate_distance(self, target_x, target_y):
        dx = abs(self.x - target_x)
        dy = abs(self.y - target_y)
        grid_size = GridConfig.GRID_SIZE
        wrapped_dx = min(dx, grid_size - dx)
        wrapped_dy = min(dy, grid_size - dy)
        return wrapped_dx + wrapped_dy

    def _find_nearest_hideout(self, world):
        if not world.hideouts:
            return None

        return min(world.hideouts, key=lambda h: self._calculate_distance(h.x, h.y))

    def _move_towards(self, target_x, target_y):
        if self.x == target_x and self.y == target_y:
            return False

        dx = target_x - self.x
        dy = target_y - self.y
        grid_size = GridConfig.GRID_SIZE

        if abs(dx) > grid_size / 2:
            dx = -1 * (grid_size - abs(dx)) * (dx / abs(dx))
        if abs(dy) > grid_size / 2:
            dy = -1 * (grid_size - abs(dy)) * (dy / abs(dy))

        move_x = 1 if dx > 0 else -1 if dx < 0 else 0
        move_y = 1 if dy > 0 else -1 if dy < 0 else 0

        moved = False

        if move_x != 0 or move_y != 0:
            self.move(move_x, move_y)

            stamina_cost = self.stamina * self.STAMINA_MOVE_COST
            self.stamina -= stamina_cost

            if self.stamina < 0:
                self.stamina = 0

            moved = True

        return moved

    def _scan_for_treasure(self, world):
        found_treasures = []

        for treasure in world.treasures:
             dist_x = abs(self.x - treasure.x)
             dist_y = abs(self.y - treasure.y)
             grid_size = GridConfig.GRID_SIZE
             wrapped_dist_x = min(dist_x, grid_size - dist_x)
             wrapped_dist_y = min(dist_y, grid_size - dist_y)

             if wrapped_dist_x <= self.SCAN_RADIUS and wrapped_dist_y <= self.SCAN_RADIUS:
                 found_treasures.append(treasure)

        if found_treasures:
            best_treasure = max(found_treasures, key=lambda t: t.value)
            return best_treasure

        return None

    def act(self, world):
        if self.is_dead:
            return

        if self.stamina <= 0:
            self.is_dead = True
            if self.carrying:
                self.carrying.x, self.carrying.y = self.x, self.y
                world.treasures.append(self.carrying)
                self.carrying = None
            return

        if self.is_caught:
            return

        if self.carrying or self.stamina <= self.STAMINA_CRITICAL_LEVEL:
            is_returning = True
            nearest_hideout = self._find_nearest_hideout(world)

            if nearest_hideout:
                if self.x == nearest_hideout.x and self.y == nearest_hideout.y:
                    if self.carrying:
                        nearest_hideout.stored_treasure.append(self.carrying)
                        self.carrying = None
                    if self.stamina <= self.STAMINA_CRITICAL_LEVEL:
                        self.stamina += self.stamina * self.RECOVERY_RATE_PERCENT
                        if self.stamina > self.MAX_STAMINA:
                            self.stamina = self.MAX_STAMINA
                else:
                    self._move_towards(nearest_hideout.x, nearest_hideout.y)
            else:
                is_returning = False

            if is_returning:
                 return

        treasure_here = world.get_treasure_at(self.x, self.y)

        if treasure_here:
            self.carrying = treasure_here
            world.treasures.remove(treasure_here)
            return

        best_nearby_treasure = self._scan_for_treasure(world)

        if best_nearby_treasure:
            self._move_towards(best_nearby_treasure.x, best_nearby_treasure.y)
            return

        dx, dy = random.choice([-1, 0, 1]), random.choice([-1, 0, 1])
        if dx != 0 or dy != 0:
             stamina_cost = self.stamina * self.STAMINA_MOVE_COST
             self.stamina -= stamina_cost
             if self.stamina < 0: self.stamina = 0
             self.move(dx, dy)


    def __repr__(self):
         return f"Hunter(Sta:{self.stamina}/{self.MAX_STAMINA}, Carry:{self.carrying is not None}, Pos:({self.x},{self.y}))"