import pygame
import sys
from config import *
from state_manager import StateManager

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Geometry Dash Clone")
    
    state_manager = StateManager(screen)
    state_manager.run()

if __name__ == "__main__":
    main()
