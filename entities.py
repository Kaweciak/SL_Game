import pygame
from enum import Enum

class State(Enum):
    PLAYING = 1
    DEAD = 2
    COMPLETE = 3

class Player:
    def __init__(self):
        self.rect = pygame.Rect(100, 100, 50, 50)
        self.velocity = pygame.Vector2(0, 0)
        self.on_ground = False
        self.spawn_point = pygame.Rect(100, 100, 50, 50)
        self.state = State.PLAYING

    def set_spawn_point(self, x, y):
        self.spawn_point = pygame.Rect(x, y, 50, 50)
        self.rect.topleft = self.spawn_point.topleft

    def respawn(self):
        self.rect.topleft = self.spawn_point.topleft
        self.velocity = pygame.Vector2(0, 0)
        self.state = State.PLAYING

    def update(self, platforms, obstacles):
        self.apply_gravity()
        self.handle_input()
        collision_result = self.handle_collisions(platforms, obstacles)
        if collision_result == State.DEAD:
            self.state = State.DEAD
        else:
            self.check_bounds()
        return self.state

    def apply_gravity(self):
        if not self.on_ground:
            self.velocity.y += 0.5  # Gravity
        else:
            self.velocity.y = 0

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_UP] and self.on_ground:
            self.velocity.y = -10

    def handle_collisions(self, platforms, obstacles):
        self.on_ground = False
        self.rect.y += self.velocity.y
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity.y > 0:
                    self.rect.bottom = platform.rect.top
                    self.on_ground = True
                elif self.velocity.y < 0:
                    self.rect.top = platform.rect.bottom
                self.velocity.y = 0
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                self.state = State.DEAD
        return self.state

    def check_bounds(self):
        if self.rect.top > pygame.display.get_surface().get_height():
            self.state = State.DEAD

    def render(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), self.rect)

class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def render(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.rect)

class Obstacle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def render(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

class FinishPoint:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def render(self, screen):
        pygame.draw.rect(screen, (0, 255, 255), self.rect)
