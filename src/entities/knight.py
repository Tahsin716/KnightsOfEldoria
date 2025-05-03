from src.entities.base_entity import BaseEntity
from src.configs.grid_config import GridConfig
import random

from src.entities.hunter import Hunter


class Knight(BaseEntity):
    SCAN_RADIUS = 3
    MAX_ENERGY = 100
    LOW_ENERGY_THRESHOLD_PERCENT = 20
    PATROL_MOVE_COST = 1
    PURSUE_MOVE_COST = 0.20
    RECOVERY_RATE_PERCENT = 0.10
    INTERACTION_STAMINA_DRAIN_PERCENT = 0.20

    def __init__(self, x, y):
        super().__init__(x, y)
        self.max_energy = self.MAX_ENERGY
        self.energy = self.max_energy
        self.is_detaining = False
        self.detained_hunter : Hunter = None

    def _calculate_distance(self, target_x, target_y):
        dx = abs(self.x - target_x); dy = abs(self.y - target_y)
        grid_size = GridConfig.GRID_SIZE
        wrapped_dx = min(dx, grid_size - dx); wrapped_dy = min(dy, grid_size - dy)
        return wrapped_dx + wrapped_dy

    def _move_towards(self, target_x, target_y):
        if self.x == target_x and self.y == target_y: return False
        dx = target_x - self.x; dy = target_y - self.y
        grid_size = GridConfig.GRID_SIZE
        if abs(dx) > grid_size / 2: dx = -1 * (grid_size - abs(dx)) * (dx / abs(dx))
        if abs(dy) > grid_size / 2: dy = -1 * (grid_size - abs(dy)) * (dy / abs(dy))
        move_x = 1 if dx > 0 else -1 if dx < 0 else 0
        move_y = 1 if dy > 0 else -1 if dy < 0 else 0
        moved = False
        if move_x != 0 or move_y != 0:
            self.move(move_x, move_y); moved = True
        return moved

    def _find_nearest_garrison(self, world):

        if not world.garrisons: return None

        return min(world.garrisons, key=lambda garrison: self._calculate_distance(garrison.x, garrison.y))


    def act(self, world):
        is_at_garrison = False
        for garrison in world.garrisons:
            if self.x == garrison.x and self.y == garrison.y:
                is_at_garrison = True
                break

        if is_at_garrison:
            if self.energy < self.max_energy:
                self.energy += self.energy * self.RECOVERY_RATE_PERCENT
                if self.energy > self.max_energy:
                    self.energy = self.max_energy
                return

        needs_to_retreat = self.energy <= self.LOW_ENERGY_THRESHOLD_PERCENT

        moved = False
        energy_cost = 0

        if needs_to_retreat:

            target_garrison = self._find_nearest_garrison(world)
            if target_garrison:
                # Move towards the garrison object's coordinates
                moved = self._move_towards(target_garrison.x, target_garrison.y)


        if not needs_to_retreat:
            target_hunter = None
            nearby_hunters = []

            for hunter in world.hunters:
                 if hunter.is_dead or (hunter.is_caught and self.detained_hunter != hunter): continue
                 distance = self._calculate_distance(hunter.x, hunter.y)
                 if distance <= self.SCAN_RADIUS:
                     nearby_hunters.append((distance, hunter))

            if nearby_hunters:
                nearby_hunters.sort(key=lambda item: item[0])
                target_hunter = nearby_hunters[0][1]
                moved = self._move_towards(target_hunter.x, target_hunter.y)
                if moved:
                    energy_cost = self.energy * self.PURSUE_MOVE_COST
            else:
                dx, dy = random.choice([-1, 0, 1]), random.choice([-1, 0, 1])
                if dx != 0 or dy != 0:
                    self.move(dx, dy)
                    moved = True

        if moved and self.energy > 0:
            self.energy -= energy_cost
            if self.energy < 0:
                self.energy = 0

        if self.energy > self.LOW_ENERGY_THRESHOLD_PERCENT:
            caught_hunter : Hunter = None

            if self.is_detaining and not self.detained_hunter.is_dead:
                caught_hunter = self.detained_hunter
            else:
                for hunter in world.hunters:
                     if not hunter.is_dead and self.x == hunter.x and self.y == hunter.y:
                         caught_hunter = hunter
                         self.detained_hunter = hunter
                         self.is_detaining = True
                         break

            if caught_hunter:
                 caught_hunter.is_caught = True
                 stamina_drain = caught_hunter.MAX_STAMINA * self.INTERACTION_STAMINA_DRAIN_PERCENT
                 caught_hunter.stamina -= stamina_drain
                 if caught_hunter.stamina <= 0:
                     caught_hunter.stamina = 0
                     caught_hunter.is_dead = True
                     caught_hunter.is_caught = False
                     self.is_detaining = False
                     self.detained_hunter = None

                 if caught_hunter.carrying:
                     dropped_treasure = caught_hunter.carrying
                     dropped_treasure.x = self.x
                     dropped_treasure.y = self.y
                     world.treasures.append(dropped_treasure)
                     caught_hunter.carrying = None


    def __repr__(self):
         return f"Knight(E:{self.energy:.1f}/{self.max_energy}, Pos:({self.x},{self.y}))"