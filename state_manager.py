
import pygame
import sys
import random
from config import *
from player import Player
from obstacle import Obstacle, ObstacleFactory
from score import Score
from difficulty import DifficultyManager
from patterns import PatternGenerator
from visuals import draw_gradient_background, draw_grid, draw_speed_lines
from particles import ParticleSystem

class State:
    def __init__(self):
        self.done = False
        self.next_state = None

    def handle_events(self, events):
        pass

    def update(self, dt):
        pass

    def render(self, screen):
        pass

    def reset(self):
        pass

class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.font = pygame.font.Font(None, 36)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surf = self.font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

class MenuState(State):
    def __init__(self):
        super().__init__()
        self.title_font = pygame.font.Font(None, 80)
        self.title_text = self.title_font.render("GEOMETRY DASH", True, BLACK)
        self.start_button = Button(300, 250, 200, 50, "Start Game", GREEN)
        self.rankings_button = Button(300, 320, 200, 50, "Rankings", BLUE)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button.is_clicked(event.pos):
                    self.done = True
                    self.next_state = "PLAYING"
                elif self.rankings_button.is_clicked(event.pos):
                    self.done = True
                    self.next_state = "RANKING"

    def render(self, screen):
        screen.fill(GRAY)
        screen.blit(self.title_text, (SCREEN_WIDTH // 2 - self.title_text.get_width() // 2, 100))
        self.start_button.draw(screen)
        self.rankings_button.draw(screen)

class PlayingState(State):
    def __init__(self):
        super().__init__()
        self.player = Player()
        self.score = Score()
        self.difficulty_manager = DifficultyManager()
        self.obstacles = []
        self.last_spawn_time = 0
        self.phase_change_timer = 0
        self.phase_change_duration = 1.5 # seconds
        self.last_phase_name = self.difficulty_manager.get_phase_name()
        self.particle_system = ParticleSystem()
        self.player_was_on_ground = True # To detect landing

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    self.player.jump()
                elif event.key == pygame.K_DOWN:
                    self.player.crouch()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.player.uncrouch()

    def update(self, dt):
        self.difficulty_manager.update(dt)
        current_speed = self.difficulty_manager.get_speed()
        current_spawn_interval = self.difficulty_manager.get_spawn_interval()
        allowed_types = self.difficulty_manager.get_allowed_types()

        # Check for phase change
        current_phase_name = self.difficulty_manager.get_phase_name()
        if current_phase_name != self.last_phase_name:
            self.phase_change_timer = self.phase_change_duration
            self.last_phase_name = current_phase_name

        if self.phase_change_timer > 0:
            self.phase_change_timer -= dt

        if self.score.current_score > self.score.high_score:
            self.score.high_score = self.score.current_score

        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time > current_spawn_interval:
            allowed_patterns = self.difficulty_manager.get_allowed_patterns()
            pattern_name = random.choice(allowed_patterns)
            new_obstacles, pattern_width = PatternGenerator.get_pattern(pattern_name, SCREEN_WIDTH, current_speed)
            self.obstacles.extend(new_obstacles)
            self.last_spawn_time = current_time + pattern_width # Add pattern width to spawn time

        self.player.apply_gravity()

        # Emit particles on landing
        if self.player.on_ground and not self.player_was_on_ground:
            self.particle_system.emit(self.player.x + self.player.width / 2, self.player.y + self.player.height, 10, WHITE, size=3, lifetime=0.5, spread=0.5)
        self.player_was_on_ground = self.player.on_ground

        obstacles_to_keep = []
        for obstacle in self.obstacles:
            obstacle.move()
            if obstacle.is_off_screen():
                # Emit particles when obstacle is passed
                self.particle_system.emit(obstacle.x + obstacle.width / 2, obstacle.y + obstacle.height / 2, 5, obstacle.get_color(), size=2, lifetime=0.3, spread=0.3)
            else:
                obstacles_to_keep.append(obstacle)
        self.obstacles = obstacles_to_keep

        if self.check_collision():
            # Emit particles on collision
            self.particle_system.emit(self.player.x + self.player.width / 2, self.player.y + self.player.height / 2, 30, RED, size=5, lifetime=1.0, spread=2.0)
            self.score.save_score()
            self.done = True
            self.next_state = "GAME_OVER"

        self.particle_system.update(dt)

    def render(self, screen):
        draw_gradient_background(screen, self.difficulty_manager.get_elapsed_time())
        draw_grid(screen, self.difficulty_manager.get_speed())
        draw_speed_lines(screen, self.difficulty_manager.get_speed())

        self.player.draw(screen)
        for obstacle in self.obstacles:
            obstacle.draw(screen)
        self.score.display(screen)

        phase_font = pygame.font.Font(None, 36)
        phase_text = phase_font.render(self.difficulty_manager.get_phase_name(), True, BLACK)
        screen.blit(phase_text, (SCREEN_WIDTH - phase_text.get_width() - 10, 10))

        if self.phase_change_timer > 0:
            phase_change_font = pygame.font.Font(None, 100)
            phase_change_text = phase_change_font.render(self.difficulty_manager.get_phase_name(), True, WHITE)
            text_rect = phase_change_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            screen.blit(phase_change_text, text_rect)
        
        self.particle_system.draw(screen)

    def check_collision(self):
        player_rect = self.player.get_rect()
        for obstacle in self.obstacles:
            if obstacle.type == 'fake':
                continue
            obstacle_rect = obstacle.get_rect()
            if player_rect.colliderect(obstacle_rect):
                return True
        return False
    
    def reset(self):
        self.player.reset()
        self.score.reset()
        self.difficulty_manager.reset()
        self.obstacles = []
        self.last_spawn_time = 0
        self.phase_change_timer = 0
        self.last_phase_name = self.difficulty_manager.get_phase_name()
        self.particle_system.reset()
        self.player_was_on_ground = True

class GameOverState(State):
    def __init__(self):
        super().__init__()
        self.title_font = pygame.font.Font(None, 80)
        self.info_font = pygame.font.Font(None, 40)
        self.play_again_button = Button(300, 300, 200, 50, "Play Again", GREEN)
        self.menu_button = Button(300, 370, 200, 50, "Menu", BLUE)
        self.score = 0
        self.high_score = 0

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_again_button.is_clicked(event.pos):
                    self.done = True
                    self.next_state = "PLAYING"
                elif self.menu_button.is_clicked(event.pos):
                    self.done = True
                    self.next_state = "MENU"

    def render(self, screen):
        screen.fill(GRAY)
        title_text = self.title_font.render("GAME OVER", True, RED)
        score_text = self.info_font.render(f"Your Score: {self.score}", True, BLACK)
        high_score_text = self.info_font.render(f"High Score: {self.high_score}", True, BLACK)
        
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 200))
        screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, 250))

        self.play_again_button.draw(screen)
        self.menu_button.draw(screen)

class RankingState(State):
    def __init__(self):
        super().__init__()
        self.title_font = pygame.font.Font(None, 60)
        self.rank_font = pygame.font.Font(None, 36)
        self.back_button = Button(300, 500, 200, 50, "Back to Menu", BLUE)
        self.rankings = Score().load_scores()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button.is_clicked(event.pos):
                    self.done = True
                    self.next_state = "MENU"

    def render(self, screen):
        screen.fill(GRAY)
        title_text = self.title_font.render("Rankings", True, BLACK)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        for i, rank in enumerate(self.rankings):
            rank_text = self.rank_font.render(f"{i+1}. {rank['score']} - {rank['date']}", True, BLACK)
            screen.blit(rank_text, (200, 120 + i * 30))

        self.back_button.draw(screen)

class StateManager:
    def __init__(self, screen):
        self.screen = screen
        self.states = {
            "MENU": MenuState(),
            "PLAYING": PlayingState(),
            "GAME_OVER": GameOverState(),
            "RANKING": RankingState()
        }
        self.current_state_name = "MENU"
        self.current_state = self.states[self.current_state_name]

    def run(self):
        clock = pygame.time.Clock()
        while True:
            dt = clock.tick(FPS) / 1000.0
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.current_state.handle_events(events)
            self.current_state.update(dt)
            self.current_state.render(self.screen)

            if self.current_state.done:
                self.flip_state()

            pygame.display.flip()

    def flip_state(self):
        previous_state_name = self.current_state_name
        next_state_name = self.current_state.next_state
        self.current_state.done = False
        self.current_state_name = next_state_name
        
        # Pass data between states
        if previous_state_name == "PLAYING" and next_state_name == "GAME_OVER":
            self.states["GAME_OVER"].score = self.states["PLAYING"].score.current_score
            self.states["GAME_OVER"].high_score = self.states["PLAYING"].score.high_score
        
        self.current_state = self.states[self.current_state_name]
        self.current_state.reset()
