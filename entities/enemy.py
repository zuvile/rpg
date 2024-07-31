from entities.character import Character
from entities.rectangle import Rectangle


class Enemy(Character):
    def __init__(self, current_map, hp, x, y):
        texture = 'assets/monsters.png'
        sub_texture = Rectangle(0, 0, 32, 32)
        scale = 1
        super().__init__(texture, sub_texture, scale, current_map, hp, x, y)
