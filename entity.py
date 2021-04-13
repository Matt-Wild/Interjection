import random

from pe2 import object


class Entity:

    def __init__(self, handler, name):
        self.handler = handler
        self.name = name


class Character(Entity):

    def __init__(self, handler, name, speed=100, health=100, base_speed=100, base_health=100, passive_state=None, icon_filename="default.png"):
        super().__init__(handler, name)
        self.speed = speed
        self.health = health

        self.base_speed = base_speed
        self.base_health = base_health

        self.state = "passive"

        if passive_state is None:
            self.passive_state = object.Image(handler, name + "Passive State", image_path="characters/default.png")
        else:
            self.passive_state = passive_state

        if icon_filename == "default.png":
            choice = random.randint(1, 5)
            icon_filename = f"default_{choice}.png"

        self.icon = object.Image(handler, f"{name} Icon", image_path=f"charIcons/{icon_filename}")
        self.icon.rescale_pwidth(0.03)

        self.icon_large = object.Image(handler, f"{name} Icon Large", image_path=f"charIcons/{icon_filename}")
        self.icon_large.rescale_pwidth(0.07)

    def update(self):
        if self.state == "passive":
            self.passive_state.update()

    def draw(self):
        if self.state == "passive":
            self.passive_state.draw()

    def prepare_for_turn(self):
        self.speed = 0

    def wait_for_turn(self):
        self.speed += self.base_speed // 10

    def rescale(self, width=None, height=None):
        self.passive_state.rescale(width, height)

    def get_p_health(self):
        return self.health / self.base_health

    def set_local_pos(self, x=None, y=None):
        if x is not None:
            self.passive_state.local_x = x

        if y is not None:
            self.passive_state.local_y = y
