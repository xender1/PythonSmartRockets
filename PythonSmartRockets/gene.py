import random
from pygame.math import Vector2

from settings import Settings

class Gene:
    """Simple Gene: direction, speed, and duration"""
    def __init__(self) -> None:
        """init a gene"""
        self.settings = Settings()

        self.direction = Vector2(0,0)
        self.speed = 0
        self.duration = 1000

        self.randomize()

    def randomize(self) -> None:
        """randomize direction, speed, and duration"""
        self.direction.x = random.randint(self.settings.MIN_VEL, self.settings.MAX_VEL)
        #-abs because up for Y is a negative value and we dont want rockets going down
        self.direction.y = -abs(random.randint(self.settings.MIN_VEL, self.settings.MAX_VEL))

        self.speed = random.uniform(self.settings.MIN_SPEED, self.settings.MAX_SPEED)

        self.duration = random.randint(self.settings.MIN_DUR, self.settings.MAX_DUR)

        