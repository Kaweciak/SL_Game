import pygame
from enum import Enum
import json

class State(Enum):
    PLAYING = 1
    DEAD = 2
    COMPLETE = 3

class Player:
    def __init__(self, spawn_x=100, spawn_y=100):
        self.rect = pygame.Rect(spawn_x, spawn_y, 50, 50)
        self.velocity = pygame.Vector2(0, 0)
        self.on_ground = False
        self.spawn_point = pygame.Rect(spawn_x, spawn_y, 50, 50)
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
            self.velocity.y += 0.5
        else:
            self.velocity.y = 0

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.velocity.x = -5
        elif keys[pygame.K_RIGHT]:
            self.velocity.x = 5
        else:
            self.velocity.x = 0
        
        if keys[pygame.K_UP] and self.on_ground:
            self.velocity.y = -10

    def handle_collisions(self, platforms, obstacles):
        self.on_ground = False

        # Vertical movement
        self.rect.y += self.velocity.y
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity.y > 0:  # Falling
                    self.rect.bottom = platform.rect.top
                    self.on_ground = True
                elif self.velocity.y < 0:  # Jumping up
                    self.rect.top = platform.rect.bottom
                self.velocity.y = 0

        # Horizontal movement
        self.rect.x += self.velocity.x
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity.x > 0:  # Moving right
                    self.rect.right = platform.rect.left
                elif self.velocity.x < 0:  # Moving left
                    self.rect.left = platform.rect.right
                self.velocity.x = 0

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

class StartPoint:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 10, 10)  # Small rectangle to represent the start point

    def render(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.rect)  # Black color for start point

class Level:
    def __init__(self, start_point, finish_points, platforms, obstacles):
        self.start_point = start_point
        self.finish_points = finish_points
        self.platforms = platforms
        self.obstacles = obstacles

    def to_dict(self):
        return {
            "start_point": (self.start_point.rect.x, self.start_point.rect.y),
            "finish_points": [
                {
                    "x": f.rect.x,
                    "y": f.rect.y,
                    "width": f.rect.width,
                    "height": f.rect.height
                } for f in self.finish_points
            ],
            "platforms": [
                {
                    "x": p.rect.x,
                    "y": p.rect.y,
                    "width": p.rect.width,
                    "height": p.rect.height
                } for p in self.platforms
            ],
            "obstacles": [
                {
                    "x": o.rect.x,
                    "y": o.rect.y,
                    "width": o.rect.width,
                    "height": o.rect.height
                } for o in self.obstacles
            ]
        }

    @classmethod
    def from_dict(self, data):
        start_point_data = data["start_point"]
        start_point = StartPoint(start_point_data[0], start_point_data[1])
        finish_points_data = data["finish_points"]
        finish_points = [FinishPoint(f["x"], f["y"], f["width"], f["height"]) for f in finish_points_data]
        platforms = [Platform(p["x"], p["y"], p["width"], p["height"]) for p in data["platforms"]]
        obstacles = [Obstacle(o["x"], o["y"], o["width"], o["height"]) for o in data["obstacles"]]
        return self(start_point, finish_points, platforms, obstacles)

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4, sort_keys=True)

    @classmethod
    def from_json(self, json_str):
        data = json.loads(json_str)
        return self.from_dict(data)
