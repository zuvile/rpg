from enum import Enum
from pyray import *
from animation.card_animations import MoveAnimation
from util.font import get_font
from config import SCREEN_WIDTH, SCREEN_HEIGHT


class CardType(Enum):
    ATTACK = 1
    HEAL = 2
    MOVE = 3
    BUFF = 4
    ADD_TO_ENEMY_PILE = 5
    ADD_TO_OWN_PILE = 6
    DEBUFF = 7


class CardParams(Enum):
    WIDTH = 64
    HEIGHT = 96


class Card:
    def __init__(self, name, type, damage, heal, buff, card=None, multiplier=0, exhaust=False):
        self.name = name
        self.type = type
        self._damage = damage
        self._health_mod = heal
        self.type = type
        self.buff = buff
        self.tmp_buff = 0
        self.start_x = 0
        self.color = RED
        self.x = 0
        self.y = 0
        self.card = card
        self.multiplier = multiplier
        self.move_animation = MoveAnimation()
        self.exhaust = exhaust
        self.width = CardParams.WIDTH.value
        self.height = CardParams.HEIGHT.value

    def play(self):
        self.move_animation.start(get_time())

    def draw(self, x, y):
        t = self.move_animation.eval(get_time())
        if t != 0:
            center_of_screen_x, center_of_screen_y = SCREEN_WIDTH // 2 - 32, SCREEN_HEIGHT // 3
            self.x = int(x + 32 + t * (center_of_screen_x - (x + 32)))
            self.y = int(y - 32 + t * (center_of_screen_y - (y - 32)))
        else:
            self.x = x
            self.y = y
        rec = Rectangle(self.x, self.y, self.width, self.height)
        draw_rectangle_pro(rec, Vector2(64, 80), 0, self.color)
        text_position = Vector2(self.x, self.y)
        draw_text_pro(get_font('default'), self.name, text_position, Vector2(64, 80), 0, 20, 1, BLACK)

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
        if self._health_mod > 0:
            return self._health_mod + self.tmp_buff
        return self._health_mod

    def clear_buff(self):
        self.tmp_buff = 0

    def animations_finished(self):
        return self.move_animation.finished(get_time())