import pygame
from pygame.math import Vector2
from math import atan2, pi

from settings import Settings
from gene import Gene

class Rocket():
    """Defines Rocket attributes"""

    def __init__(self, screen: pygame.Surface) -> None:
        """Init a rocket"""
        self.settings = Settings()

        self.surface = pygame.Surface(self.settings.R_SIZE, pygame.SRCALPHA)
        self.surface.fill(self.settings.white)
        self.rect = self.surface.get_rect()

        self.rotated_surface = self.surface
        self.rotated_rect = self.rect
        self.angle = 0

        self.position = Vector2(screen.get_rect().midbottom)
        self.position.y -= self.settings.R_SIZE.y

        self.rect.x = int(self.position.x)
        self.rect.y = int(self.position.y)

        self.velocity = Vector2(0, 0)

        self.is_alive = True

        self.start_time = pygame.time.get_ticks()
        self.curr_time = self.start_time

        self.cur_gene = 0


        self.genes: list[Gene] = []
        for i in range(self.settings.GENE_SIZE):
            self.genes.append(Gene())

        self.velocity = self.genes[self.cur_gene].velocity


    def update(self, screen: pygame.Surface) -> None:
        """Update position of the rocket"""

        #check if we need to move to the next gene velocity
        #see if the current genes time is up and if so move to the next one
        self.curr_time = pygame.time.get_ticks() - self.start_time
        if self.curr_time > self.genes[self.cur_gene].duration:
            print("new gene")
            self.setVelocityFromGenes()
            self.start_time = pygame.time.get_ticks()
            self.curr_time = self.start_time

        self.position = self.position + self.velocity

        self.rect.x = int(self.position.x)
        self.rect.y = int(self.position.y)

        self.checkWallCollision(screen)

        #now we rotate the object based on velocity direction
        #MATH!
        self.angle = atan2(self.velocity.x, self.velocity.y) * 180 / pi
        self.rotated_surface = pygame.transform.rotate(self.surface, self.angle)
        self.rotated_rect = self.rotated_surface.get_rect(center=self.rect.center)

    def setVelocityFromGenes(self):
        """Set velocity from the next genes value"""
        #TODO: need to check timer
        self.cur_gene += 1
        if self.cur_gene == self.settings.GENE_SIZE:
            self.cur_gene = 0

        self.velocity = self.genes[self.cur_gene].velocity


    def checkWallCollision(self, screen: pygame.Surface):
        """Check if the rocket hits a wall and stop it (currently reverse direction)"""
        #TODO: should set is_alive to false
        #TODO: needs to be rotated rect
        if self.rect.left < 0 or self.rect.right > screen.get_width():
            self.velocity.x *= -1
        if self.rect.top < 0 or self.rect.bottom > screen.get_height():
            self.velocity.y *= -1


    def blitme(self, screen: pygame.Surface) -> None:
        """Draw to screen"""
        screen.blit(self.rotated_surface, self.rotated_rect)

    