from config import *

PHASES = [
    {'name': 'Tutorial', 'duration': 20, 'speed_mult': 1.0, 'spawn_interval': 2000, 'types': ['basic', 'tall'], 'patterns': ['SINGLE']},
    {'name': 'Warmup', 'duration': 20, 'speed_mult': 1.2, 'spawn_interval': 1800, 'types': ['basic', 'tall', 'low', 'double'], 'patterns': ['SINGLE', 'DOUBLE']},
    {'name': 'Challenge', 'duration': 20, 'speed_mult': 1.5, 'spawn_interval': 1600, 'types': ['basic', 'tall', 'low', 'double', 'triangle', 'moving'], 'patterns': ['SINGLE', 'DOUBLE', 'STAIRS_UP']},
    {'name': 'Hard', 'duration': 20, 'speed_mult': 1.8, 'spawn_interval': 1400, 'types': ['basic', 'tall', 'double', 'triangle', 'moving', 'fake', 'spike'], 'patterns': ['DOUBLE', 'STAIRS_UP']},
    {'name': 'Extreme', 'duration': 20, 'speed_mult': 2.0, 'spawn_interval': 1200, 'types': ['double', 'triangle', 'moving', 'spike', 'tunnel_top'], 'patterns': ['STAIRS_UP']},
    {'name': 'Endgame', 'duration': 999, 'speed_mult': 2.5, 'spawn_interval': 1000, 'types': ['triangle', 'moving', 'spike', 'tunnel_top', 'tunnel_bottom'], 'patterns': ['STAIRS_UP']}
]

class DifficultyManager:
    def __init__(self):
        self.current_phase_index = 0
        self.elapsed_time = 0

    def update(self, dt):
        self.elapsed_time += dt
        if self.current_phase_index < len(PHASES) - 1:
            if self.elapsed_time > self.get_current_phase()['duration']:
                self.elapsed_time = 0
                self.current_phase_index += 1

    def get_current_phase(self):
        return PHASES[self.current_phase_index]

    def get_speed(self):
        phase = self.get_current_phase()
        return OBSTACLE_BASE_SPEED * phase['speed_mult']

    def get_spawn_interval(self):
        return self.get_current_phase()['spawn_interval']

    def get_allowed_types(self):
        return self.get_current_phase()['types']

    def get_allowed_patterns(self):
        return self.get_current_phase()['patterns']

    def get_phase_name(self):
        return self.get_current_phase()['name']

    def get_elapsed_time(self):
        return self.elapsed_time

    def reset(self):
        self.current_phase_index = 0
        self.elapsed_time = 0
