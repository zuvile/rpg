from pyray import *
from entities.character import Character


class Friendly(Character):
    rel = 0
    def __init__(self, x=0, y=0):
        texture = load_texture('assets/dorian.png')
        sub_texture = Rectangle(0, 0, 32, 32)
        scale = 2

        super().__init__(texture, sub_texture, scale, x, y)

    def talk(self):
        return "Hello! I am a friendly character."
