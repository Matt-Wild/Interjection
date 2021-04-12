from pe2 import object


class Entity:

    def __init__(self, handler, name):
        self.handler = handler
        self.name = name


class Character(Entity):

    def __init__(self, handler, name, speed=100, health=100, base_speed=100, base_health=100, passive_state=None):
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
