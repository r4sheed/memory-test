# game_logic.py

import random

class GameLogic:
    def __init__(self):
        self.current_numbers = []

    def generate_unique_numbers(self, count, range_min, range_max):
        self.current_numbers = random.sample(range(range_min, range_max + 1), count)
        return self.current_numbers
