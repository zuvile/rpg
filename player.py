from character import Character
from collision import should_init_fight
from pyray import *
from actions import *

class Player(Character):
    def __init__(self, x=0, y=0):
        texture = load_texture('assets/free_character_1-3.png')
        sub_texture = Rectangle(48, 0, 15, 20)
        scale = 2

        super().__init__(texture, sub_texture, scale, x, y)
    def move(self, dx, dy, map):
        if self.can_move(dx, dy, map):
            self.rec.x += dx
            self.rec.y += dy
        if should_init_fight(self, map):
            return Actions.FIGHT
