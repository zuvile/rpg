from entities.character import Character
from entities.rectangle import Rectangle


class Enemy(Character):
    def __init__(self, deck, current_map, hp, x, y):
        texture = 'assets/monsters.png'
        sub_texture = Rectangle(0, 0, 32, 32)
        scale = 1
        self.move_speed = 1.0
        self.last_move_time = 0
        self.path_index = 0
        self.path = []
        #todo change this
        super().__init__(texture, sub_texture, scale, deck, current_map, hp, x, y)
