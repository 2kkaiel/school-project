import pygame
import math
from config import *

def draw_gradient_background(screen, time_elapsed):
    # Define color sets for interpolation
    sky_blue = (135, 206, 235)
    purple = (128, 0, 128)
    pink = (255, 192, 203)

    # Interpolate between colors using a sine wave for smooth transition
    t = (math.sin(time_elapsed * 0.1) + 1) / 2 # Varies between 0 and 1

    if t < 0.5:
        color1 = sky_blue
        color2 = purple
        interp_t = t * 2
    else:
        color1 = purple
        color2 = pink
        interp_t = (t - 0.5) * 2

    start_color = [
        color1[0] + (color2[0] - color1[0]) * interp_t,
        color1[1] + (color2[1] - color1[1]) * interp_t,
        color1[2] + (color2[2] - color1[2]) * interp_t
    ]
    end_color = [
        start_color[0] * 0.5,
        start_color[1] * 0.5,
        start_color[2] * 0.5
    ]

    # Draw gradient
    for y in range(SCREEN_HEIGHT):
        color = [
            start_color[0] + (end_color[0] - start_color[0]) * (y / SCREEN_HEIGHT),
            start_color[1] + (end_color[1] - start_color[1]) * (y / SCREEN_HEIGHT),
            start_color[2] + (end_color[2] - start_color[2]) * (y / SCREEN_HEIGHT)
        ]
        pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))

def draw_speed_lines(screen, speed):
    num_lines = int(speed * 2)
    for i in range(num_lines):
        x = (pygame.time.get_ticks() * speed / 5 + i * 100) % SCREEN_WIDTH
        y = (i * 50) % SCREEN_HEIGHT
        alpha = int(100 + (speed / MAX_OBSTACLE_SPEED) * 155)
        alpha = max(0, min(255, alpha))
        line_color = (255, 255, 255, alpha)
        
        s = pygame.Surface((10, 2), pygame.SRCALPHA)
        s.fill(line_color)
        screen.blit(s, (x, y))

def draw_grid(screen, speed):
    scroll_speed = speed
    offset = (pygame.time.get_ticks() * scroll_speed / 20) % 40
    for x in range(0, SCREEN_WIDTH, 40):
        pygame.draw.line(screen, DARK_GRAY, (x - offset, 0), (x - offset, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, 40):
        pygame.draw.line(screen, DARK_GRAY, (0, y), (SCREEN_WIDTH, y))
