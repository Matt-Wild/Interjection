import random

import entity


class PlayerData:

    def __init__(self, handler):
        self.handler = handler
        self.team_layout = []
        self.reset_team_layout()

    def reset_team_layout(self):
        self.team_layout = [[None, None, None], [None, None, None], [None, None, None]]

    def add_random_character(self):
        if self.check_for_free_slot():
            addition = entity.Character(self.handler, "Character", random.randint(50, 100), random.randint(50, 100))

            conflict = True
            while conflict:
                x = random.randint(0, 2)
                y = random.randint(0, 2)

                if self.team_layout[x][y] is None:
                    self.team_layout[x][y] = addition
                    conflict = False

    def check_for_free_slot(self):
        for column in self.team_layout:
            for character in column:
                if character is None:
                    return True
        return False
