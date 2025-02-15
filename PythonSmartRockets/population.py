import pygame

from settings import Settings
from rocket import Rocket

#TODO: think about moving the Rockets update/draw to screen function in here \
#instead of in the gameengine functions

class Population:
    """Class to hold a population of rockets"""
    def __init__(self, screen: pygame.Surface) -> None:
        """Create base population based on settings (rocket #, gene #, etc)"""
        self.settings = Settings()

        self.is_complete = False
        self.generation = 1

        self.rockets: list[Rocket] = []

        for i in range(self.settings.POP_SIZE):
            self.rockets.append(Rocket(screen))


    #TODO: im not sure this is needed (// there is a better way to write this)
    def isComplete(self) -> bool:
        """Check if all the rockets are done"""
        self.is_complete = True
        for rock in self.rockets:
            if rock.is_alive:
                self.is_complete = False

        return self.is_complete
    
