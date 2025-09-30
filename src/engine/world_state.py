from dataclasses import dataclass
from typing import List, Tuple

from systems.procedural_gen import generate_map


@dataclass
class WorldState:
    width: int
    height: int
    map: List[List[str]] = None # type: ignore

    def __post_init__(self):
        self.map = generate_map(self.width, self.height)
        self.player_pos = (1, 1)
        self.enemies = [(5,5)]

    def process_player_command(self, cmd: str):
        x,y = self.player_pos
        if cmd == "w": y -= 1
        if cmd == "s": y += 1
        if cmd == "a": x -= 1
        if cmd == "d": x += 1
        # checar colisoes simples e limites
        if 0 <= x < self.width and 0 <= y < self.height and self.map[y][x] == ".":
            self.player_pos = (x,y)

    def update_enemies(self):
        # placeholder: mover inimigos aleatoriamente
        pass
