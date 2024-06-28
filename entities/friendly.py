from pyray import *
from entities.character import Character


class Friendly(Character):
    def __init__(self, x=0, y=0):
        texture = load_texture('assets/dorian.png')
        sub_texture = Rectangle(0, 0, 32, 32)
        scale = 2
        self.rel = 0

        super().__init__(texture, sub_texture, scale, x, y)
