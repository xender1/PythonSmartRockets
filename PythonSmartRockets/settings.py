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
        self.POP_SIZE = 4
        self.GENE_SIZE = 4

        #some rocket settings
        self.R_SIZE = Vector2(10, 50)

        #some gene settings
        self.MIN_VEL = -6
        self.MAX_VEL = 6

        self.MIN_DUR = 500
        self.MAX_DUR = 5000





        #Some colors to play with (i dont like this actually, use pygame colors?)
        self.red = (255, 0 , 0)
        self.green = (0, 255, 0)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.blue = (0,0, 255)
        self.purple = (99, 14, 107)

