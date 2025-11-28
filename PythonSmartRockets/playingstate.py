import pygame
from typing import Optional

from settings import Settings
from textgui import TextGUI
from population import Population


class PlayingState:
    """Playing state - handles gameplay"""

    def __init__(self, screen: pygame.Surface) -> None:
        """Initialize playing state"""
        self.settings = Settings()
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # UI Labels
        self.generation_counter = TextGUI(self.screen, "Generation: 1", self.screen_rect.topleft)
        self.best_score_label = TextGUI(self.screen, "Best Score: 0", (0, self.generation_counter.msg_rect.bottom))
        self.title_label = TextGUI(self.screen, "Rocket Testing", self.screen_rect.topright)
        self.title_label.msg_rect.topright = self.screen_rect.topright

        self.best_score = 0

        # Population of rockets
        self.population = Population(self.screen)

        # Target to hit
        self.target = pygame.Rect(
            self.settings.screen_center.x,
            self.settings.screen_center.y - 300,
            35, 35
        )

        # DEBUG
        print(f"Rocket count: {len(self.population.rockets)}")
        for i, rocket in enumerate(self.population.rockets):
            genes_info = [(g.direction, g.speed, g.duration) for g in rocket.genes]
            print(f"Rocket {i} Genes: {genes_info}")

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """Handle events for playing state. Returns action string or None."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                return "pause"
        return None

    def update(self) -> None:
        """Update game logic"""
        # Check if all rockets are dead, if so restart population
        if not self.population.checkIsRunning():
            self.population.restart(self.screen, self.target)

        # Update all rockets
        for rock in self.population.rockets:
            rock.update(self.screen, self.target)

    def draw(self) -> None:
        """Draw game elements"""
        # Update and draw generation counter
        self.generation_counter.update_text(f"Generation: {self.population.generation}")
        self.generation_counter.draw_text(self.screen)

        # Update best score from all rockets
        for rock in self.population.rockets:
            if rock.score > self.best_score:
                self.best_score = rock.score

        # Draw best score
        self.best_score_label.update_text(f"Best Score: {self.best_score}")
        self.best_score_label.draw_text(self.screen)

        # Draw title label
        self.title_label.draw_text(self.screen)

        # Draw target
        pygame.draw.rect(self.screen, self.settings.purple, self.target)

        # Draw rockets
        for rock in self.population.rockets:
            rock.blitme(self.screen)
