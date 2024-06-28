from entities.character import Character
from collision import should_init_fight, should_init_dialogue
from pyray import *
from actions import *


class Player(Character):
    def __init__(self, x=0, y=0):
        texture = load_texture('assets/player.png')
        sub_texture = Rectangle(0, 0, 32, 32)
        scale = 2
        self.attack = 10
        self.ac = 5
        self.hp = 30
        self.magic = 1
        self.mana = 10
        self.dead = False

        super().__init__(texture, sub_texture, scale, x, y)

    def move(self, map):
        if is_key_down(KEY_W):
            return self.move_player(0, -2, map)
        if is_key_down(KEY_S):
            return self.move_player(0, 2, map)
        if is_key_down(KEY_A):
            return self.move_player(-2, 0, map)
        if is_key_down(KEY_D):
            return self.move_player(2, 0, map)
        return Actions.EXPLORE

    def move_player(self, dx, dy, map):
        if self.can_move(dx, dy, map):
            self.rec.x += dx
            self.rec.y += dy
        if should_init_fight(self, map):
            return Actions.FIGHT
        if should_init_dialogue(self, map):
            return Actions.DIALOGUE
        else:
            return Actions.EXPLORE

    def increase_magic_skill(self, modifier):
        self.magic += modifier