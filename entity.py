class Entity:

    def __init__(self, name):
        self.name = name


class Character(Entity):

    def __init__(self, name, speed=100):
        super().__init__(name)
        self.speed = speed
