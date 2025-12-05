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
        # Ensure direction is never (0, 0)
        while True:
            self.direction.x = random.randint(self.settings.MIN_VEL, self.settings.MAX_VEL)
            #-abs because up for Y is a negative value and we dont want rockets going down
            self.direction.y = -abs(random.randint(self.settings.MIN_VEL, self.settings.MAX_VEL))
            if self.direction.x != 0 and self.direction.y != 0:
                break

        self.speed = random.randint(self.settings.MIN_SPEED, self.settings.MAX_SPEED)

        self.duration = random.randint(self.settings.MIN_DUR, self.settings.MAX_DUR)

    def copy(self) -> 'Gene':
        """Create a copy of this gene"""
        new_gene = Gene.__new__(Gene) #skips __init__
        new_gene.settings = self.settings
        new_gene.direction = Vector2(self.direction.x, self.direction.y)
        new_gene.speed = self.speed
        new_gene.duration = self.duration
        return new_gene

    def mutate(self) -> None:
        """Slightly mutate gene values instead of fully randomizing"""
        # Mutate direction, keep trying until we get a valid direction
        while True:
            new_x = self.direction.x + random.randint(-self.settings.MUTATE_DIRECTION_RANGE, self.settings.MUTATE_DIRECTION_RANGE)
            new_y = self.direction.y + random.randint(-self.settings.MUTATE_DIRECTION_RANGE, self.settings.MUTATE_DIRECTION_RANGE)

            # Keep direction in valid range
            new_x = max(self.settings.MIN_VEL, min(self.settings.MAX_VEL, new_x))
            # -abs because up for Y is a negative value and we dont want rockets going down
            new_y = -abs(max(self.settings.MIN_VEL, min(self.settings.MAX_VEL, new_y)))

            # Ensure direction is never (0, 0)
            if new_x != 0 or new_y != 0:
                self.direction.x = new_x
                self.direction.y = new_y
                break

        # Mutate speed
        self.speed += random.randint(-self.settings.MUTATE_SPEED_RANGE, self.settings.MUTATE_SPEED_RANGE)
        self.speed = max(self.settings.MIN_SPEED, min(self.settings.MAX_SPEED, self.speed))

        # Mutate duration
        self.duration += random.randint(-self.settings.MUTATE_DURATION_RANGE, self.settings.MUTATE_DURATION_RANGE)
        self.duration = max(self.settings.MIN_DUR, min(self.settings.MAX_DUR, self.duration))
