from time import sleep

from rich.console import Console

from engine.world_state import WorldState
from renderer.terminal_ui import TerminalUI


class GameLoop:
    def __init__(self):
        self.console = Console()
        self.world = WorldState(width=40, height=20)
        self.ui = TerminalUI(self.console, self.world)
        self.running = True

    def run(self):
        while self.running:
            self.ui.render()
            command = self.ui.get_input()
            if command == "q":
                self.running = False
                break
            self.world.process_player_command(command)
            self.world.update_enemies()
            sleep(0.03)
        self.console.print("Saindo... Obrigado por jogar.")
