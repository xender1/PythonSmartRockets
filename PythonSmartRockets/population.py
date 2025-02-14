import pygame

from settings import Settings

from rocket import Rocket

class Population:
    """Class to hold a population of rockets"""
    def __init__(self, screen: pygame.Surface) -> None:
        """Create base population based on settings (rocket #, gene #, etc)"""
        self.settings = Settings()

        self.generation = 1

        self.rockets: list[Rocket] = []

        for i in range(self.settings.POP_SIZE):
            self.rockets.append(Rocket(screen))

