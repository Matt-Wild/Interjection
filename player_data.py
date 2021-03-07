import random

import entity


class PlayerData:

    def __init__(self):
        self.team_layout = []
        self.reset_team_layout()

    def reset_team_layout(self):
        self.team_layout = [[None, None, None], [None, None, None], [None, None, None]]

    def add_random_character(self):
        if None in self.team_layout:
            addition = entity.Character("Character", random.randint(50, 100))

            conflict = True
            while conflict:
                x = random.randint(0, 2)
                y = random.randint(0, 2)
                self.team_layout[x][y] = addition
