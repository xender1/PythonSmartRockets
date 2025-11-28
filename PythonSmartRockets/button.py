import pygame
from typing import Tuple

from settings import Settings


class Button:
    """A clickable button class"""

    def __init__(self, screen: pygame.Surface, msg: str, center: Tuple[int, int]) -> None:
        """Initialize button attributes"""
        self.settings = Settings()
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Button dimensions and properties
        self.width = 200
        self.height = 50
        self.button_color = (0, 135, 0)
        self.hover_color = (0, 200, 0)
        self.text_color = self.settings.white
        self.font = pygame.font.SysFont("Arial", 32)

        # Build the button's rect and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = center

        self._prep_msg(msg)

    def _prep_msg(self, msg: str) -> None:
        """Render message into an image and center on button"""
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw(self, mouse_pos: Tuple[int, int]) -> None:
        """Draw button to screen with hover effect"""
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(self.screen, self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def is_clicked(self, mouse_pos: Tuple[int, int]) -> bool:
        """Check if button was clicked"""
        return self.rect.collidepoint(mouse_pos)
