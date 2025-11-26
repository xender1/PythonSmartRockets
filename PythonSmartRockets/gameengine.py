import pygame
from pygame.math import Vector2
import sys

from settings import Settings
from textgui import TextGUI

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
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption(self.settings.caption)

        #TODO: make font here and pass it in to TextGUI to reuse.
        self.generation_counter = TextGUI(self.screen, "Generation: 1", self.screen_rect.topleft)
        self.best_score_label = TextGUI(self.screen, "Best Score: 0", (0, self.generation_counter.msg_rect.bottom))
        self.title_label = TextGUI(self.screen, "Rocket Test", self.screen_rect.topright)
        # Adjust position so text doesn't go off screen (anchor by topright instead of topleft)
        self.title_label.msg_rect.topright = self.screen_rect.topright

        self.best_score = 0

        #population of rockets        
        self.new_pop = Population(self.screen)

        #simple target to hit
        self.target = pygame.Rect(self.settings.screen_center.x, self.settings.screen_center.y - 300,
                                                         35, 35)

        #DEBUG
        print(f"Rocket count: {len(self.new_pop.rockets)}")
        for i, rocket in enumerate(self.new_pop.rockets):
            genes_info = [(g.direction, g.speed, g.duration) for g in rocket.genes]
            print(f"Rocket {i} Genes: {genes_info}")


    def run_game(self) -> None:
        """Start main game loop"""
        print("run_game")

        self.start_tick = pygame.time.get_ticks()
        while True:
            #check for events
            self._check_events()

            #Check if all rockets are dead, if so restart pop
            #TODO: will be mutations first
            if not self.new_pop.checkIsRunning():
                self.new_pop.restart(self.screen, self.target)

            #update objects pos/values
            #TODO: move this into a population function
            #   self.new_pop.update()
            for rock in self.new_pop.rockets:
                rock.update(self.screen, self.target)


            self._draw_screen()

            self.clock.tick(self.settings.frame_rate)

            '''
            seconds = (pygame.time.get_ticks() - self.start_tick) / 1000
            if seconds > 5:
                print("5 seconds")
                
                DEBUG
                for rock in self.new_pop.rockets:
                    rock.setVelocityFromGenes()

                print(self.new_pop.rockets[0].velocity)
                
                self.start_tick = pygame.time.get_ticks()
            '''


    def _check_events(self) -> None:
        """Check for keyboard/mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

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

        # Update and draw generation counter
        self.generation_counter.update_text(f"Generation: {self.new_pop.generation}")
        self.generation_counter.draw_text(self.screen)

        # Update best score from all rockets
        for rock in self.new_pop.rockets:
            if rock.score > self.best_score:
                self.best_score = rock.score

        # Draw best score
        self.best_score_label.update_text(f"Best Score: {self.best_score}")
        self.best_score_label.draw_text(self.screen)

        # Draw title label
        self.title_label.draw_text(self.screen)

        pygame.draw.rect(self.screen, self.settings.purple, self.target)

        for rock in self.new_pop.rockets:
            rock.blitme(self.screen)

        pygame.display.flip()


if __name__ == '__main__':
    ge = GameEngine()
    ge.run_game()

