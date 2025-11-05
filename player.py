import pygame
from config import *

class Player:
    def __init__(self):
        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.original_height = PLAYER_HEIGHT
        self.color = BLUE
        self.velocity_y = 0
        self.is_jumping = False
        self.on_ground = True
        self.double_jump_available = True
        self.is_crouching = False

        # Visual polish attributes
        self.rotation_angle = 0
        self.squash_factor = 1.0
        self.trail_positions = []

    def jump(self):
        if self.on_ground:
            self.velocity_y = PLAYER_JUMP_FORCE
            self.is_jumping = True
            self.on_ground = False
            self.rotation_angle = -30
        elif not self.on_ground and self.double_jump_available:
            self.velocity_y = PLAYER_JUMP_FORCE * 0.8 # Make double jump slightly weaker
            self.double_jump_available = False
            self.rotation_angle = -30

    def apply_gravity(self):
        # Update trail
        self.trail_positions.append((self.x, self.y, self.width, self.height * self.squash_factor))
        if len(self.trail_positions) > 5:
            self.trail_positions.pop(0)

        self.velocity_y += PLAYER_GRAVITY
        self.y += self.velocity_y

        # Gradual rotation back to 0
        self.rotation_angle += (0 - self.rotation_angle) * 0.2

        # Squash and stretch
        self.squash_factor += (1.0 - self.squash_factor) * 0.2

        if self.y >= GROUND_Y - self.height:
            if not self.on_ground: # Just landed
                self.squash_factor = 0.8
            self.y = GROUND_Y - self.height
            self.velocity_y = 0
            self.on_ground = True
            self.is_jumping = False
            self.double_jump_available = True

    def crouch(self):
        if not self.is_crouching and self.on_ground:
            self.is_crouching = True
            self.height = self.original_height / 2
            self.y += self.original_height / 2

    def uncrouch(self):
        if self.is_crouching:
            self.is_crouching = False
            self.height = self.original_height
            self.y -= self.original_height / 2

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        # Draw trail
        for i, pos in enumerate(self.trail_positions):
            alpha = int(255 * (i / len(self.trail_positions)) * 0.5)
            trail_color = (*self.color, alpha)
            s = pygame.Surface((pos[2], pos[3]), pygame.SRCALPHA)
            s.fill(trail_color)
            screen.blit(s, (pos[0], pos[1]))

        # Create surface for the player
        player_surface = pygame.Surface((self.width, self.height * self.squash_factor), pygame.SRCALPHA)
        player_surface.fill(self.color)

        # Rotate the surface
        rotated_surface = pygame.transform.rotate(player_surface, self.rotation_angle)
        rotated_rect = rotated_surface.get_rect(center=self.get_rect().center)

        screen.blit(rotated_surface, rotated_rect.topleft)

    def reset(self):
        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y
        self.height = self.original_height
        self.velocity_y = 0
        self.is_jumping = False
        self.on_ground = True
        self.double_jump_available = True
        self.is_crouching = False
        self.rotation_angle = 0
        self.squash_factor = 1.0
        self.trail_positions = []
