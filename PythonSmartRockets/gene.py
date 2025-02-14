import random
from pygame.math import Vector2

from settings import Settings

class Gene:
    """Simple Gene: velocity and duration"""
    def __init__(self) -> None:
        """init a gene"""
        self.settings = Settings()

        self.velocity = Vector2(0,0)
        self.duration = 1000

        self.randomize()

    def randomize(self) -> None:
        """randomize velocity and duration"""
        self.velocity.x = random.randint(self.settings.MIN_VEL, self.settings.MAX_VEL)
        self.velocity.y = -abs(random.randint(self.settings.MIN_VEL, self.settings.MAX_VEL))
        
        self.duration = random.randint(self.settings.MIN_DUR, self.settings.MAX_DUR)
