from time import sleep

from rich.console import Console
from rich.live import Live

from engine.world_state import WorldState
from renderer.terminal_ui import TerminalUI
from systems.ai_system import simple_ai_system
from systems.fov_system import system_update_fov


class GameLoop:
    """
    Classe principal do loop do jogo.
    Gerencia o estado do mundo, entrada do jogador e renderização.
    """
    def __init__(self):
        self.console = Console()
        self.world = WorldState(width=40, height=20)
        self.ui = TerminalUI(self.console, self.world)
        self.running = True

    def run(self):
        with Live(console=self.console, refresh_per_second=30) as live:
            while self.running and not self.world.game_over:
                system_update_fov(self.world)
                self.ui.render()
                command = self.ui.get_input()
                if command == "q":
                    self.running = False
                    break
                player_took_turn = self.world.process_player_command(command)
                if player_took_turn:
                    simple_ai_system(self.world)
                sleep(0.03)
            self.console.print("Saindo... Obrigado por jogar.")
