from entities.character import Character
from entities.rectangle import Rectangle

class Enemy(Character):
    def __init__(self, x=0, y=0):
        texture = 'assets/free_character_1-3.png'
        sub_texture = Rectangle(0, 0, 16, 16)
        scale = 2

        super().__init__(texture, sub_texture, scale, x, y)
