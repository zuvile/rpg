from enum import Enum


class CardType(Enum):
    ATTACK = 1
    HEAL = 2
    MOVE = 3
    BUFF = 4


class Card:
    def __init__(self, name, type, damage, heal, range, buff):
        self.types = [
            'ATTACK',
            'HEAL',
            'MOVE',
            'BUFF',
        ]
        self.name = name
        self.type = type
        self._damage = damage
        self._heal = heal
        self._range = range
        self.type = type
        self.buff = buff
        self.tmp_buff = 0

    def get_description(self):
        if self.type == CardType.ATTACK:
            return f"Damage: {self.get_damage()}\n, Range: {self.get_range()}\n"
        elif self.type == CardType.HEAL:
            return f"Heal: {self.get_heal()}\n"
        elif self.type == CardType.MOVE:
            return f"Move Range: {self.get_range()}\n"
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

    def get_range(self):
        if self._range > 0:
            return self._range + self.tmp_buff
        return self._range

    def clear_buff(self):
        self.tmp_buff = 0
