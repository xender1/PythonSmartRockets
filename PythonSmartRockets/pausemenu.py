import pygame
from typing import Optional

from settings import Settings
from textgui import TextGUI
from button import Button


class PauseMenu:
    """Pause menu overlay"""

    def __init__(self, screen: pygame.Surface) -> None:
        """Initialize pause menu"""
        self.settings = Settings()
        self.screen = screen
        self.screen_rect = screen.get_rect()

        center_x = self.settings.screen_width // 2
        center_y = self.settings.screen_height // 2

        # Pause label
        self.title = TextGUI(self.screen, "PAUSED", (center_x, center_y), "Arial", 48)
        self.title.msg_rect.center = (center_x, center_y)

        # Resume button
        self.resume_button = Button(self.screen, "Resume", (center_x, center_y + 60))

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """Handle events for pause menu. Returns action string or None."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                return "resume"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.resume_button.is_clicked(mouse_pos):
                return "resume"
        return None

    def draw(self) -> None:
        """Draw pause menu overlay"""
        mouse_pos = pygame.mouse.get_pos()
        self.title.draw_text(self.screen)
        self.resume_button.draw(mouse_pos)
