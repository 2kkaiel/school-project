import pygame
import random
from config import *

class Particle:
    def __init__(self, x, y, vx, vy, color, size, lifetime):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.age = 0

    def update(self, dt):
        self.x += self.vx * dt * 60 # Scale velocity by dt
        self.y += self.vy * dt * 60
        self.vy += PLAYER_GRAVITY * dt * 60 # Apply gravity to particles
        self.age += dt
        return self.age > self.lifetime

    def draw(self, screen):
        alpha = max(0, 255 - int(255 * (self.age / self.lifetime)))
        if len(self.color) == 3:
            color_with_alpha = (*self.color, alpha)
        else:
            color_with_alpha = (self.color[0], self.color[1], self.color[2], alpha)

        s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, color_with_alpha, (self.size, self.size), self.size)
        screen.blit(s, (self.x - self.size, self.y - self.size))

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def emit(self, x, y, count, color, size=5, lifetime=1.0, spread=1.0):
        for _ in range(count):
            vx = random.uniform(-spread, spread)
            vy = random.uniform(-spread, spread)
            self.particles.append(Particle(x, y, vx, vy, color, size, lifetime))

    def update(self, dt):
        self.particles = [p for p in self.particles if not p.update(dt)]

    def draw(self, screen):
        for p in self.particles:
            p.draw(screen)

    def reset(self):
        self.particles = []
