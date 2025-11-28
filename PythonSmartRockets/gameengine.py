import pygame
import sys
from enum import Enum

from settings import Settings
from mainmenu import MainMenu
from pausemenu import PauseMenu
from playingstate import PlayingState


class GameState(Enum):
    """Enum for game states"""
    MENU = 1
    PLAYING = 2
    PAUSED = 3


class GameEngine:
    """Overall class to handle game assets and behavior"""

    def __init__(self) -> None:
        """Initialize game and create game resources with Pygame"""
        self.settings = Settings()

        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption(self.settings.caption)

        # Game state
        self.game_state = GameState.MENU

        # Initialize state classes
        self.main_menu = MainMenu(self.screen)
        self.pause_menu = PauseMenu(self.screen)
        self.playing_state = PlayingState(self.screen)

    def run_game(self) -> None:
        """Start main game loop"""
        print("run_game")

        while True:
            self._check_events()

            # Only update game logic when playing
            if self.game_state == GameState.PLAYING:
                self.playing_state.update()

            self._draw_screen()

            self.clock.tick(self.settings.frame_rate)

    def _check_events(self) -> None:
        """Check for keyboard/mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()

            # Delegate events to current state
            if self.game_state == GameState.MENU:
                action = self.main_menu.handle_event(event)
                if action == "start":
                    self.game_state = GameState.PLAYING

            elif self.game_state == GameState.PLAYING:
                action = self.playing_state.handle_event(event)
                if action == "pause":
                    self.game_state = GameState.PAUSED

            elif self.game_state == GameState.PAUSED:
                action = self.pause_menu.handle_event(event)
                if action == "resume":
                    self.game_state = GameState.PLAYING

    def _draw_screen(self) -> None:
        """Draw objects to screen"""
        self.screen.fill(self.settings.black)

        if self.game_state == GameState.MENU:
            self.main_menu.draw()
        elif self.game_state == GameState.PLAYING:
            self.playing_state.draw()
        elif self.game_state == GameState.PAUSED:
            self.playing_state.draw()
            self.pause_menu.draw()

        pygame.display.flip()


if __name__ == '__main__':
    ge = GameEngine()
    ge.run_game()
