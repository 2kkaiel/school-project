import pygame
import json
import os
from datetime import datetime
from operator import itemgetter
from config import *

class Score:
    def __init__(self):
        self.current_score = 0
        self.high_score = 0
        self.rankings = self.load_scores()
        if self.rankings:
            self.high_score = self.rankings[0]['score']

    def increment(self, amount=1):
        self.current_score += amount

    def reset(self):
        self.current_score = 0

    def save_score(self):
        score_data = {
            'score': self.current_score,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.rankings.append(score_data)
        self.rankings = sorted(self.rankings, key=itemgetter('score'), reverse=True)[:10]

        try:
            os.makedirs(os.path.dirname(SCORE_FILE), exist_ok=True)
            with open(SCORE_FILE, 'w') as f:
                json.dump(self.rankings, f, indent=2)
        except IOError as e:
            print(f"Error saving score: {e}")

    def load_scores(self):
        try:
            with open(SCORE_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def get_rankings(self):
        return self.rankings

    def display(self, screen):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.current_score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        if self.high_score > 0:
            high_score_text = font.render(f"High Score: {self.high_score}", True, BLACK)
            screen.blit(high_score_text, (10, 50))
