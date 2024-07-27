from enum import Enum
from pyray import *


class CardType(Enum):
    ATTACK = 1
    HEAL = 2
    MOVE = 3
    BUFF = 4
    ADD_TO_ENEMY_PILE = 5
    ADD_TO_OWN_PILE = 6
    DEBUFF = 7


class Card:
    def __init__(self, name, type, damage, heal, buff, card=None, multiplier=0, exhaust=False):
        self.name = name
        self.type = type
        self._damage = damage
        self._heal = heal
        self.type = type
        self.buff = buff
        self.tmp_buff = 0
        self.start_x = 0
        self.color = RED
        self.x = 0
        self.y = 0
        self.is_moving = False
        self.move_animation_start = 0
        self.card = card
        self.multiplier = multiplier

    def play(self):
        self.is_moving = True
        self.move_animation_start = get_time()

    def draw(self, x, y):
        if self.is_moving:
            self.draw_movement()
            return
        else:
            self.x = x
            self.y = y
        draw_rectangle(self.x + 32, self.y - 32, 128, 160, self.color)
        draw_text(self.name, self.x + 32, self.y - 32, 20, BLACK)
        # draw_text(self.get_description(), dec_x + 32,dec_y, 12, BLACK)
        # if self.tmp_buff != 0:
        #     draw_text("+ " + str(self.tmp_buff), dec_x + 32, dec_y + 32, 20, BLACK)

    def draw_movement(self):
        if get_time() - self.move_animation_start > 2:
            self.is_moving = False
            return
        center_of_screen_x, center_of_screen_y = get_screen_width() // 2 - 32, get_screen_height() // 3

        if self.x < center_of_screen_x:
            self.x += 32
        if self.x > center_of_screen_x:
            self.x -= 32
        if self.y < center_of_screen_y:
            self.y += 32
        if self.y > center_of_screen_y:
            self.y -= 32
        draw_rectangle(self.x, self.y, 128, 160, self.color)
        draw_text(self.name, self.x + 32, self.y - 32, 20, BLACK)
        draw_text(self.get_description(), self.x + 32, self.y, 12, BLACK)

    def get_description(self):
        if self.type == CardType.ATTACK:
            return f"Damage: {self.get_damage()}\n"
        elif self.type == CardType.HEAL:
            return f"Heal: {self.get_heal()}\n"
        elif self.type == CardType.BUFF:
            return f"Buff all current cards: {self.buff}\n"

    def set_tmp_buff(self, buff):
        self.tmp_buff = buff

    def get_damage(self):
        if self._damage > 0:
            return self._damage + self.tmp_buff
        return self._damage

    def get_heal(self):
        if self._heal > 0:
            return self._heal + self.tmp_buff
        return self._heal

    def clear_buff(self):
        self.tmp_buff = 0
