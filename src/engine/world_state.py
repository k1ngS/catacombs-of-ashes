import random
from dataclasses import dataclass
from typing import List, Tuple

from systems.ecs import AI, Combat, Position, Renderable
from systems.procedural_gen import generate_map


@dataclass
class WorldState:
    width: int
    height: int
    map: List[List[str]] = None # type: ignore

    def __post_init__(self):
        self.world = {
            Position: {},
            Renderable: {},
            Combat: {},
            AI: {},
        }
        self.next_entity_id = 0

        self.map = generate_map(self.width, self.height)

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

    # --- Auxiliary methods of ecs ---
    def create_entity(self) -> int:
        """Generate a new unique entity ID."""
        entity_id = self.next_entity_id
        self.next_entity_id += 1
        return entity_id

    def create_player(self, x: int, y: int):
        player_id = self.create_entity()
        self.world[Position][player_id] = Position(x, y)
        self.world[Renderable][player_id] = Renderable(symbol='@', color='bright_green')
        self.world[Combat][player_id] = Combat(current_hp=10, max_hp=10, attack=2, defense=1)

        self.player_id = player_id

    def create_enemy(self, x: int, y: int):
        enemy_id = self.create_entity()
        self.world[Position][enemy_id] = Position(x, y)
        self.world[Renderable][enemy_id] = Renderable('g', 'red')
        self.world[Combat][enemy_id] = Combat(5, 5, 1, 0)
        self.world[AI][enemy_id] = AI()

    def process_player_command(self, cmd: str):
        post_component = self.world[Position][self.player_id]
        x, y = post_component.x, post_component.y

        if cmd == "w": y -= 1
        if cmd == "s": y += 1
        if cmd == "a": x -= 1
        if cmd == "d": x += 1

        # checar colisoes simples e limites
        if 0 <= x < self.width and 0 <= y < self.height and self.map[y][x] == "[grey50]░[/]":
            post_component.x, post_component.y = x, y

            return True
        return False