from entities.character import Character
from entities.rectangle import Rectangle

class Friendly(Character):
    def __init__(self, name, portrait, x=0, y=0):
        texture = 'assets/dorian.png'
        sub_texture = Rectangle(0, 0, 32, 32)
        self.portrait = portrait
        self.name = name
        scale = 2
        self.rel = 0

        super().__init__(texture, sub_texture, scale, x, y)

