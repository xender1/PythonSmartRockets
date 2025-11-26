from pygame.math import Vector2

class Settings:
    """Store settings for Smart Rockets"""

    def __init__(self) -> None:
        """Game settings"""
        self.caption: str = "Smart Rocket Testing"

        #Screen settings
        self.screen_width = 1200
        self.screen_height = 800

        self.screen_center = Vector2(self.screen_width / 2, self.screen_height / 2)

        self.bg_color = (100, 230, 230)

        self.frame_rate = 60


        self.DEBUG = False


        #some population of rocket settings
        self.POP_SIZE = 10
        self.GENE_SIZE = 10

        #some rocket settings
        self.R_SIZE = Vector2(5, 30)

        #some gene settings
        self.MIN_VEL = -4
        self.MAX_VEL = 4

        self.MIN_SPEED = 1
        self.MAX_SPEED = 5

        self.MIN_DUR = 100
        self.MAX_DUR = 3000

        self.MUTATE_SINGLE_GENE_CHANCE = 10
        self.MUTATE_ALL_GENE_CHANCE = 3




        #Some colors to play with 
        #TODO: (i dont like this actually, use pygame colors?)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0 , 0)
        self.green = (0, 255, 0)
        self.blue = (0,0, 255)
        self.purple = (128, 0, 128)

