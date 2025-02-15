import pygame
from pygame.math import Vector2

from settings import Settings


#TODO: this might be overkill and just do it in main
class TextGUI:
    """Class for displaying text to screen"""

    #font: Font
    def __init__(self, screen: pygame.Surface, msg: str, pos) -> None:
        """Basic text attributes"""

        #to display text on the screen:
        #create a pygame.font object, call render on that object to make a surface
        #blit surface to screen
        #after getting the text surface, get_rect and can better position etc.

        self.settings = Settings()

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.font = pygame.font.SysFont("Arial", 18)
        self.txt_color = self.settings.white

        self.msg_surf = self.font.render(msg, True, self.txt_color)
        self.msg_rect = self.msg_surf.get_rect()
        self.msg_rect.topleft = pos

    def draw_text(self, screen: pygame.Surface) -> None:
        """Draw txt image to the screen"""
        self.screen.blit(self.msg_surf, self.msg_rect)


    #TODO:
    #just init basic stuff and then declare stuff like this
    #this iss where we can figure out the rect size etc and place it correclty on screen
    def prep_image(self):
        pass
    
    def draw_top_left(self):
        pass

    def draw_top_right(self):
        pass

    def draw_at_location(self):
        pass

