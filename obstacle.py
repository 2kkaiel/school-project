import pygame
import random
from config import *

class Obstacle:
    def __init__(self, x, y, width, height, speed=OBSTACLE_BASE_SPEED, type='basic'):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.type = type
        self.rect = pygame.Rect(x, y, width, height)

        if self.type == 'moving':
            self.vertical_speed = 2
            self.vertical_direction = 1
            self.vertical_limit_top = y - 50
            self.vertical_limit_bottom = y + 50

    def get_color(self):
        if self.type == 'basic':
            return RED
        elif self.type == 'tall':
            return (200, 0, 0) # DARK_RED
        elif self.type == 'low':
            return (255, 165, 0) # ORANGE
        elif self.type == 'triangle':
            return (128, 0, 128) # PURPLE
        elif self.type == 'moving':
            return (255, 192, 203) # PINK
        elif self.type == 'fake':
            color = list(GRAY)
            color.append(128) # Add alpha for transparency
            return tuple(color)
        elif self.type == 'spike':
            return (75, 0, 130) # DARK_PURPLE
        elif self.type == 'tunnel_top' or self.type == 'tunnel_bottom':
            return DARK_GRAY
        return RED

    def move(self):
        self.x -= self.speed
        self.rect.x = self.x

        if self.type == 'moving':
            self.y += self.vertical_speed * self.vertical_direction
            if self.y <= self.vertical_limit_top or self.y >= self.vertical_limit_bottom:
                self.vertical_direction *= -1
            self.rect.y = self.y

    def is_off_screen(self):
        return self.x + self.width < 0

    def get_rect(self):
        return self.rect

    def draw(self, screen):
        color = self.get_color()
        if self.type == 'fake':
            s = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            s.fill(color)
            screen.blit(s, (self.x, self.y))
        elif self.type == 'triangle':
            points = [
                (self.x, self.y + self.height),
                (self.x + self.width / 2, self.y),
                (self.x + self.width, self.y + self.height)
            ]
            pygame.draw.polygon(screen, color, points)
        elif self.type == 'spike':
            spike_width = self.width / 5
            for i in range(5):
                points = [
                    (self.x + i * spike_width, self.y + self.height),
                    (self.x + (i + 0.5) * spike_width, self.y),
                    (self.x + (i + 1) * spike_width, self.y + self.height)
                ]
                pygame.draw.polygon(screen, color, points)
        else:
            pygame.draw.rect(screen, color, self.rect)

class ObstacleFactory:
    @staticmethod
    def create_by_type(obstacle_type, x, current_speed):
        if obstacle_type == 'basic':
            height = random.randint(OBSTACLE_MIN_HEIGHT, OBSTACLE_MAX_HEIGHT)
            y = GROUND_Y - height
            return [Obstacle(x, y, OBSTACLE_WIDTH, height, speed=current_speed, type=obstacle_type)]
        elif obstacle_type == 'tall':
            height = OBSTACLE_HEIGHT * 1.5
            y = GROUND_Y - height
            return [Obstacle(x, y, OBSTACLE_WIDTH, height, speed=current_speed, type=obstacle_type)]
        elif obstacle_type == 'low':
            height = OBSTACLE_HEIGHT * 0.5
            y = GROUND_Y - height
            return [Obstacle(x, y, OBSTACLE_WIDTH, height, speed=current_speed, type=obstacle_type)]
        elif obstacle_type == 'double':
            height = random.randint(OBSTACLE_MIN_HEIGHT, OBSTACLE_MAX_HEIGHT)
            y = GROUND_Y - height
            return [
                Obstacle(x, y, OBSTACLE_WIDTH, height, speed=current_speed, type='basic'),
                Obstacle(x + OBSTACLE_WIDTH + 100, y, OBSTACLE_WIDTH, height, speed=current_speed, type='basic')
            ]
        elif obstacle_type == 'triangle':
            height = 60
            width = 50
            y = GROUND_Y - height
            return [Obstacle(x, y, width, height, speed=current_speed, type=obstacle_type)]
        elif obstacle_type == 'moving':
            height = random.randint(OBSTACLE_MIN_HEIGHT, OBSTACLE_MAX_HEIGHT)
            y = GROUND_Y - 150
            return [Obstacle(x, y, OBSTACLE_WIDTH, height, speed=current_speed, type=obstacle_type)]
        elif obstacle_type == 'tunnel':
            top_height = 150
            bottom_height = 80
            return [
                Obstacle(x, 0, OBSTACLE_WIDTH, top_height, speed=current_speed, type='tunnel_top'),
                Obstacle(x, GROUND_Y - bottom_height, OBSTACLE_WIDTH, bottom_height, speed=current_speed, type='tunnel_bottom')
            ]
        # Add other types as needed
        return []
