import sys
import termios
import tty
from typing import Tuple

from rich.console import Console
from rich.table import Table

from systems.ecs import Position, Renderable


class TerminalUI:
    def __init__(self, console: Console, world):
        self.console = console
        self.world = world

    def render(self):
        self.console.clear()
        table = Table.grid(padding=0)
        # Gather entities with Position and Renderable components
        # Key: tuple(x, y), Value: render system
        entities_for_render = {}
        for id_entity, pos_component in self.world.world[Position].items():
            # Verify if entity has Renderable component
            if id_entity in self.world.world[Renderable]:
                render_component = self.world.world[Renderable][id_entity]
                # Added to dictionary for rendering
                entities_for_render[(pos_component.x, pos_component.y)] = render_component

        # Render the map with entities
        for y in range(self.world.height):
            row = ""
            for x in range(self.world.width):
                current_coords = (x, y)
                if current_coords in entities_for_render:
                    # Get symbol and color from Renderable component
                    symbol = entities_for_render[current_coords].symbol
                    color = entities_for_render[current_coords].color
                    row += f"[{color}]{symbol}[/{color}]"
                else:
                    if not self.world.explored_map[y][x]:
                        row += " "
                    else:
                        row += self.world.map[y][x]

            table.add_row(row)
        self.console.print(table)

        self.console.print("\n--- Log ---")
        for message in self.world.message_log:
            self.console.print(message)

    def get_input(self) -> str:
        # ler um único char sem enter (unix)
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return ch
