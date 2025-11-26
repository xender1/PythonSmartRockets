import pygame
from pygame.math import Vector2
from math import atan2, pi

from settings import Settings
from gene import Gene

class Rocket():
    """Defines Rocket attributes"""

    def __init__(self, screen: pygame.Surface, rocket_num: int) -> None:
        """Init a rocket"""
        self.settings = Settings()

        self.rocket_num = rocket_num

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

        self.direction = Vector2(0, 0)
        self.speed = 0

        self.is_alive = True
        self.hit_target = False

        self.start_time = pygame.time.get_ticks()
        self.curr_time = self.start_time
        self.total_time = 0

        self.cur_gene = 0

        # Scoring
        self.score = 0
        self.final_distance = 0

        self.genes: list[Gene] = []
        for i in range(self.settings.GENE_SIZE):
            self.genes.append(Gene())

        self.direction = self.genes[self.cur_gene].direction
        self.speed = self.genes[self.cur_gene].speed


    def update(self, screen: pygame.Surface, target: pygame.Rect) -> None:
        """Update position of the rocket"""

        if self.is_alive == False:
            if self.score == 0:
                self.calculateScore(target)
            return

        self.total_time += 1
        #check if we need to move to the next gene direction/speed
        #see if the current genes time is up and if so move to the next one
        self.curr_time = pygame.time.get_ticks() - self.start_time
        if self.curr_time > self.genes[self.cur_gene].duration:
            print(f"{self.rocket_num}: new gene")
            self.setDirectionFromGenes()
            self.start_time = pygame.time.get_ticks()
            self.curr_time = self.start_time

        # Calculate velocity from direction and speed
        if self.direction.length() > 0:
            velocity = self.direction.normalize() * self.speed
        else:
            velocity = Vector2(0, 0)

        self.position = self.position + velocity

        self.rect.x = int(self.position.x)
        self.rect.y = int(self.position.y)

        self.checkWallCollision(screen)
        self.checkTargetCollision(target)

        #now we rotate the object based on direction, MATH!
        self.angle = atan2(self.direction.x, self.direction.y) * 180 / pi
        self.rotated_surface = pygame.transform.rotate(self.surface, self.angle)
        self.rotated_rect = self.rotated_surface.get_rect(center=self.rect.center)

    def setDirectionFromGenes(self):
        """Set direction and speed from the next genes value"""

        self.cur_gene += 1
        if self.cur_gene == self.settings.GENE_SIZE:
            self.cur_gene = 0

        self.direction = self.genes[self.cur_gene].direction
        self.speed = self.genes[self.cur_gene].speed


    def checkWallCollision(self, screen: pygame.Surface):
        """Check if the rocket hits a wall and stop it"""
        #TODO: needs to be rotated rect
        if self.rect.left < 0 or self.rect.right > screen.get_width():
            self.is_alive = False
            #self.velocity.x *= -1
        if self.rect.top < 0 or self.rect.bottom > screen.get_height():
            self.is_alive = False
            #self.velocity.y *= -1

    
    def checkTargetCollision(self, target: pygame.Rect):
        """Check if rocket hit the target and stop it"""

        if self.rect.colliderect(target):
            print(f"{self.rocket_num} hit target!")
            self.is_alive = False
            self.hit_target = True

    def calculateScore(self, target: pygame.Rect):
        """Calculate score based on distance to target and time taken (1-100)"""
        target_center = Vector2(target.center)
        self.final_distance = self.position.distance_to(target_center)

        # Max possible distance (corner to corner of screen)
        max_distance = Vector2(self.settings.screen_width, self.settings.screen_height).length()

        # Distance score: closer = higher (0-50 points)
        distance_score = (1 - self.final_distance / max_distance) * 50

        # Time score: faster = higher (0-50 points)
        # Assume max reasonable time is ~10 seconds at 60fps = 600 frames
        max_frames = 600
        time_score = max(0, (1 - self.total_time / max_frames)) * 50

        # Bonus for hitting target
        if self.hit_target:
            distance_score = 50  # Max distance score

        self.score = int(max(1, min(100, distance_score + time_score)))

        print(f"DScore: {distance_score}. TScore: {time_score}. Total: {self.score}.")

    def restart(self, screen: pygame.Surface):
        """restart all rockets to start pos/gene"""
        self.position = Vector2(screen.get_rect().midbottom)
        self.position.y -= self.settings.R_SIZE.y

        self.rect.x = int(self.position.x)
        self.rect.y = int(self.position.y)

        self.is_alive = True
        self.hit_target = False

        self.start_time = pygame.time.get_ticks()
        self.curr_time = self.start_time
        self.total_time = 0

        self.cur_gene = 0

        # Reset scoring
        self.score = 0
        self.final_distance = 0

        self.direction = self.genes[self.cur_gene].direction
        self.speed = self.genes[self.cur_gene].speed

        


    def blitme(self, screen: pygame.Surface) -> None:
        """Draw to screen"""
        screen.blit(self.rotated_surface, self.rotated_rect)

    