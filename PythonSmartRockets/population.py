import pygame
import random
from pygame.math import Vector2

from settings import Settings
from rocket import Rocket
from gene import Gene

#TODO: think about moving the Rockets update/draw to screen function in here \
#instead of in the gameengine functions

class Population:
    """Class to hold a population of rockets"""
    def __init__(self, screen: pygame.Surface) -> None:
        """Create base population based on settings (rocket #, gene #, etc)"""
        self.settings = Settings()

        self.is_running = True
        self.generation = 1

        self.rockets: list[Rocket] = []

        for i in range(self.settings.POP_SIZE):
            self.rockets.append(Rocket(screen, i))


    #TODO: im not sure this is needed (// there is a better way to write this)
    def checkIsRunning(self) -> bool:
        """Check if all the rockets are done"""

        #If any rocket is alive, keep running, else false
        self.is_running = False
        for rock in self.rockets:
            if rock.is_alive:
                self.is_running = True
                break

        #if not self.is_running:
        #    print(f"All rockets dead. Scores: {[r.score for r in self.rockets]}")

        return self.is_running
    
    def restart(self, screen: pygame.Surface, target: pygame.Rect) -> None:
        """Reset all rockets to OG position and start again"""
        self.generation += 1
        self.is_running = True

        # Calculate scores for any rockets that haven't been scored yet
        for rock in self.rockets:
            if rock.score == 0:
                rock.calculateScore(target)
        print(f"All rockets dead. Scores: {[r.score for r in self.rockets]}")
        # Breed new generation before restarting
        self._breed_new_generation(screen)

        for rock in self.rockets:
            rock.restart(screen)

        print(f"# of rockets:{len(self.rockets)}")

    def _breed_new_generation(self, screen: pygame.Surface) -> None:
        """Create new generation through breeding based on scores"""
        # Sort rockets by score (highest first)
        sorted_rockets = sorted(self.rockets, key=lambda r: r.score, reverse=True)
        best_rocket = sorted_rockets[0]
        second_best = sorted_rockets[1]

        print(f"Best: {best_rocket.score}, Second: {second_best.score}")

        new_rockets: list[Rocket] = []

        # First child: best and second best mate
        child1 = self._create_child(screen, best_rocket, second_best, len(new_rockets))
        new_rockets.append(child1)

        # Rest of the children: top 2 mate with remaining rockets
        for i in range(1, self.settings.POP_SIZE):
            # Pick other parent (60% best, 40% second best)
            if random.random() < 0.6:
                parent1 = best_rocket
            else:
                parent1 = second_best

            # Pick the other parent from remaining rockets
            other_parent = sorted_rockets[i % len(sorted_rockets)]

            child = self._create_child(screen, parent1, other_parent, len(new_rockets))
            new_rockets.append(child)

        self.rockets = new_rockets

    def _create_child(self, screen: pygame.Surface, better_parent: Rocket, other_parent: Rocket, rocket_num: int) -> Rocket:
        """Create a child rocket from two parents"""
        child = Rocket(screen, rocket_num)

        # For each gene, check for mutation first, then inherit from parents
        for i in range(len(child.genes)):
            # Chance to mutate into a new random gene
            if random.randint(1, 100) <= self.settings.MUTATE_SINGLE_GENE_CHANCE:
                print("Mutation")
                child.genes[i] = Gene()  # New random gene
            # 70% chance from better parent, 30% from other
            elif random.random() < 0.7:
                child.genes[i] = better_parent.genes[i].copy()
            else:
                child.genes[i] = other_parent.genes[i].copy()

        # Set initial direction and speed from first gene (copy to avoid reference issues)
        child.direction = Vector2(child.genes[0].direction.x, child.genes[0].direction.y)
        child.speed = child.genes[0].speed

        return child
