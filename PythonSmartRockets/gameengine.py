import pygame
from pygame.math import Vector2
import sys
from enum import Enum

from settings import Settings
from textgui import TextGUI
from button import Button

from rocket import Rocket
from population import Population


class GameState(Enum):
    """Enum for game states"""
    MENU = 1
    PLAYING = 2
    PAUSED = 3

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
        self.title_label = TextGUI(self.screen, "Rocket Testing", self.screen_rect.topright)
        # Adjust position so text doesn't go off screen (anchor by topright instead of topleft)
        self.title_label.msg_rect.topright = self.screen_rect.topright

        self.best_score = 0

        # Game state
        self.game_state = GameState.MENU

        # Menu buttons (centered, Start above Exit)
        center_x = self.settings.screen_width // 2
        center_y = self.settings.screen_height // 2

        # Menu title label
        self.menu_title = TextGUI(self.screen, "Rocket Testing", (center_x, center_y - 120))
        self.menu_title.font = pygame.font.SysFont("Arial", 48)
        self.menu_title.update_text("Rocket Testing")
        self.menu_title.msg_rect.center = (center_x, center_y - 120)

        self.start_button = Button(self.screen, "Start", (center_x, center_y - 40))
        self.exit_button = Button(self.screen, "Exit", (center_x, center_y + 40))

        # Resume button for pause screen
        self.resume_button = Button(self.screen, "Resume", (center_x, center_y + 60))
        
        # Pause label (centered on screen)
        self.pause_label = TextGUI(self.screen, "PAUSED", (center_x, center_y))
        self.pause_label.font = pygame.font.SysFont("Arial", 48)
        self.pause_label.update_text("PAUSED")
        self.pause_label.msg_rect.center = (center_x, center_y)



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

            # Only update game logic when playing
            if self.game_state == GameState.PLAYING:
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_mouse_events(event)

    def _check_keydown_events(self, event) -> None:
        """Process keydown events"""
        if event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_p:
            # Toggle pause when playing or paused
            if self.game_state == GameState.PLAYING:
                self.game_state = GameState.PAUSED
            elif self.game_state == GameState.PAUSED:
                self.game_state = GameState.PLAYING

    def _check_keyup_events(self, event) -> None:
        """Process keyup events"""
        pass

    def _check_mouse_events(self, event) -> None:
        """Process mouse click events"""
        mouse_pos = pygame.mouse.get_pos()

        if self.game_state == GameState.MENU:
            if self.start_button.is_clicked(mouse_pos):
                self.game_state = GameState.PLAYING
            elif self.exit_button.is_clicked(mouse_pos):
                sys.exit()
        elif self.game_state == GameState.PAUSED:
            if self.resume_button.is_clicked(mouse_pos):
                self.game_state = GameState.PLAYING


    def _draw_screen(self) -> None:
        """Draw objects to screen"""
        self.screen.fill(self.settings.black)

        mouse_pos = pygame.mouse.get_pos()

        if self.game_state == GameState.MENU:
            self._draw_menu(mouse_pos)
        elif self.game_state == GameState.PLAYING:
            self._draw_game()
        elif self.game_state == GameState.PAUSED:
            self._draw_game()
            self._draw_pause(mouse_pos)

        pygame.display.flip()

    def _draw_menu(self, mouse_pos) -> None:
        """Draw main menu screen"""
        self.menu_title.draw_text(self.screen)
        self.start_button.draw(mouse_pos)
        self.exit_button.draw(mouse_pos)

    def _draw_game(self) -> None:
        """Draw game elements"""
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

    def _draw_pause(self, mouse_pos) -> None:
        """Draw pause overlay"""
        self.pause_label.draw_text(self.screen)
        self.resume_button.draw(mouse_pos)


if __name__ == '__main__':
    ge = GameEngine()
    ge.run_game()

