from pe2 import object


class Entity:

    def __init__(self, handler, name):
        self.handler = handler
        self.name = name


class Character(Entity):

    def __init__(self, handler, name, speed=100, passive_state=None):
        super().__init__(handler, name)
        self.speed = speed

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

    def rescale(self, width=None, height=None):
        self.passive_state.rescale(width, height)

    def set_local_pos(self, x=None, y=None):
        if x is not None:
            self.passive_state.local_x = x

        if y is not None:
            self.passive_state.local_y = y
