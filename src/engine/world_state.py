import random
from dataclasses import dataclass
from typing import List, Tuple

from systems.ecs import AI, Combat, Direction, Position, Renderable
from systems.procedural_gen import generate_map


@dataclass
class WorldState:
    width: int
    height: int
    map: List[List[str]] = None # type: ignore

    def __post_init__(self):
        self.game_over = False
        self.world = {
            Position: {},
            Direction: {},
            Renderable: {},
            Combat: {},
            AI: {},
        }
        self.next_entity_id = 0
        self.map = generate_map(self.width, self.height)
        self.visible_tiles = []
        self.explored_map = [[False for _ in range(self.width)] for _ in range(self.height)]

        self.message_log = []

        # Get free positions to place entities
        free_positions = self._find_free_position()

        # Verify there are enough free positions to place entities safely
        if not free_positions:
            raise ValueError("No free positions available on the map to place entities.")

        # Create player and enemies at predefined positions for simplicity
        player_pos = random.choice(free_positions)
        self.create_player(player_pos[0], player_pos[1])

        free_positions.remove(player_pos)  # Ensure enemy doesn't spawn on player

        if free_positions:
            enemy_pos = random.choice(free_positions)
            self.create_enemy(enemy_pos[0], enemy_pos[1])

    def _find_free_position(self) -> list[tuple[int, int]]:
        """Find all free positions on the map."""
        free_positions = []
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] == "[grey50]░[/]":
                    free_positions.append((x, y))
        return free_positions

    def process_player_command(self, cmd: str):
        pos_component = self.world[Position][self.player_id]
        dir_component = self.world[Direction][self.player_id]
        x, y = pos_component.x, pos_component.y

        if cmd == "w":
            y -= 1
            dir_component.dx, dir_component.dy = 0, -1
        if cmd == "s":
            y += 1
            dir_component.dx, dir_component.dy = 0, 1
        if cmd == "a":
            x -= 1
            dir_component.dx, dir_component.dy = -1, 0
        if cmd == "d":
            x += 1
            dir_component.dx, dir_component.dy = 1, 0

        # Calculate new position and validate
        new_position = (x, y)
        target_id = self.get_entity_at_position(*new_position)
        if target_id is not None:
            if target_id in self.world[Combat]:
                # Initiate combat
                from systems.combat_system import system_resolve_combat
                system_resolve_combat(self, self.player_id, target_id)
                return True
            return False  # Position occupied by another entity


        # checar colisoes simples e limites
        elif 0 <= x < self.width and 0 <= y < self.height and self.map[y][x] == "[grey50]░[/]":
            pos_component.x, pos_component.y = x, y
            return True

        return False

    def get_entity_at_position(self, x: int, y: int) -> int | None:
        for entity_id, pos in self.world[Position].items():
            if pos.x == x and pos.y == y:
                return entity_id
        return None


    # --- Auxiliary methods of world logs ---
    def add_message(self, text: str):
        self.message_log.append(text)
        MAX_LOG_SIZE = 5
        if len(self.message_log) > MAX_LOG_SIZE:
            self.message_log.pop(0)

    # --- Auxiliary methods of ecs ---
    def create_entity(self) -> int:
        """Generate a new unique entity ID."""
        entity_id = self.next_entity_id
        self.next_entity_id += 1
        return entity_id

    def remove_entity(self, entity_id: int):
        """Remove an entity and all its components from the world."""
        for component in self.world.values():
            component.pop(entity_id, None)

    def create_player(self, x: int, y: int):
        player_id = self.create_entity()
        self.world[Position][player_id] = Position(x, y)
        self.world[Direction][player_id] = Direction(dx=0, dy=1)  # Default facing down
        self.world[Renderable][player_id] = Renderable(symbol='@', color='bright_green')
        self.world[Combat][player_id] = Combat(current_hp=10, max_hp=10, attack=2, defense=1)

        self.player_id = player_id

    def create_enemy(self, x: int, y: int):
        enemy_id = self.create_entity()
        self.world[Position][enemy_id] = Position(x, y)
        self.world[Renderable][enemy_id] = Renderable(symbol='g', color='red')
        self.world[Combat][enemy_id] = Combat(current_hp=5, max_hp=5, attack=1, defense=0)
        self.world[AI][enemy_id] = AI()
