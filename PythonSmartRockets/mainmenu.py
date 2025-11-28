import pygame
import sys
from typing import Optional

from settings import Settings
from textgui import TextGUI
from button import Button


class MainMenu:
    """Main menu screen"""

    def __init__(self, screen: pygame.Surface) -> None:
        """Initialize main menu"""
        self.settings = Settings()
        self.screen = screen
        self.screen_rect = screen.get_rect()

        center_x = self.settings.screen_width // 2
        center_y = self.settings.screen_height // 2

        # Menu title label
        self.title = TextGUI(self.screen, "Rocket Testing", (center_x, center_y - 120), "Arial", 48)
        self.title.msg_rect.center = (center_x, center_y - 120)

        # Buttons
        self.start_button = Button(self.screen, "Start", (center_x, center_y - 40))
        self.exit_button = Button(self.screen, "Exit", (center_x, center_y + 40))

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """Handle events for main menu. Returns action string or None."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.start_button.is_clicked(mouse_pos):
                return "start"
            elif self.exit_button.is_clicked(mouse_pos):
                sys.exit()
        return None

    def draw(self) -> None:
        """Draw main menu"""
        mouse_pos = pygame.mouse.get_pos()
        self.title.draw_text(self.screen)
        self.start_button.draw(mouse_pos)
        self.exit_button.draw(mouse_pos)
