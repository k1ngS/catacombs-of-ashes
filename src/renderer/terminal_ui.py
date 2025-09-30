from rich.console import Console
from rich.table import Table
from typing import Tuple
import sys
import tty
import termios

class TerminalUI:
    def __init__(self, console: Console, world):
        self.console = console
        self.world = world

    def render(self):
        self.console.clear()
        table = Table.grid(padding=0)
        for y in range(self.world.height):
            row = ""
            for x in range(self.world.width):
                if (x,y) == self.world.player_pos:
                    row += "@"
                elif (x,y) in self.world.enemies:
                    row += "e"
                else:
                    row += self.world.map[y][x]
            table.add_row(row)
        self.console.print(table)

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
