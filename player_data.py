import random

import entity


class PlayerData:

    def __init__(self, handler):
        self.handler = handler
        self.team_layout = []
        self.reset_team_layout()

        self.random_count = 0

    def reset_team_layout(self):
        self.team_layout = [[None, None, None], [None, None, None], [None, None, None]]

    def add_random_character(self):
        self.random_count += 1

        if self.check_for_free_slot():
            speed = random.randint(50, 100)
            health = random.randint(50, 100)
            addition = entity.Character(self.handler, f"Character {self.random_count}", speed, health, speed, health)

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

    def get_next_turn(self):
        fastest_character = None

        for column in self.team_layout:
            for character in column:
                if character:
                    if not fastest_character:
                        fastest_character = character
                    elif character.speed > fastest_character.speed:
                        fastest_character.wait_for_turn()
                        fastest_character = character
                    else:
                        character.wait_for_turn()
        fastest_character.prepare_for_turn()

        return fastest_character
