import pygame
from pygame.math import Vector2
import sys

from settings import Settings

from rocket import Rocket
from population import Population

class GameEngine:
    """Overall class to handle game assets and behavior"""

    def __init__(self) -> None:
        """Initialize game and create game resources with Pygame"""
        self.settings = Settings()

        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption(self.settings.caption)


        self.new_rock = Rocket(self.screen)

        self.new_pop = Population(self.screen)

        print(len(self.new_pop.rockets))

        for i in range(len(self.new_pop.rockets)):
            print(i)
            for j in range(len(self.new_pop.rockets[i].genes)):
                print(self.new_pop.rockets[i].genes[j].velocity)


    def run_game(self) -> None:
        """Start main game loop"""
        print("run_game")

        self.start_tick = pygame.time.get_ticks()
        while True:
            #check for events
            self._check_events()

            #update objects pos/values
            self.new_rock.update(self.screen)

            for rock in self.new_pop.rockets:
                rock.update(self.screen)


            self._draw_screen()

            self.clock.tick(self.settings.frame_rate)

            seconds = (pygame.time.get_ticks() - self.start_tick) / 1000
            if seconds > 5:
                print("5 seconds")

                for rock in self.new_pop.rockets:
                    rock.setVelocityFromGenes()

                print(self.new_pop.rockets[0].velocity)
                self.start_tick = pygame.time.get_ticks()


    def _check_events(self) -> None:
        """Check for keyboard/mouse events"""
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

    def _check_keydown_events(self, event) -> None:
        """Process keydown events"""
        if event.key == pygame.K_q:
           sys.exit()
    
    def _check_keyup_events(self, event) -> None:
        """Process keyup events"""
        pass


    def _draw_screen(self) -> None:
        """Draw objects to screen"""
        self.screen.fill(self.settings.black)

        #self.new_rock.blitme(self.screen)

        for rock in self.new_pop.rockets:
            rock.blitme(self.screen)

        pygame.display.flip()


if __name__ == '__main__':
    ge = GameEngine()
    ge.run_game()

