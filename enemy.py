from character import Character
from pyray import *

class Enemy(Character):
    def __init__(self, x=0, y=0):
        texture = load_texture('assets/free_character_1-3.png')
        sub_texture = Rectangle(0, 0, 15, 20)
        scale = 2

        super().__init__(texture, sub_texture, scale, x, y)
