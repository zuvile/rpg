from enum import Enum


class CardType(Enum):
    ATTACK = 1
    HEAL = 2
    MOVE = 3


class Card:
    def __init__(self, name, type, damage, heal, range, mana_cost, mana_gain):
        self.types = [
            'ATTACK',
            'HEAL',
            'MOVE',
        ]
        self.name = name
        self.type = type
        self.damage = damage
        self.heal = heal
        self.range = range
        self.mana_cost = mana_cost
        self.mana_gain = mana_gain
        self.type = type
        self.description = self.make_description()

    def use(self, player, enemy):
        if player.mana < self.mana_cost:
            return "Not enough mana"
        player.mana -= self.mana_cost
        enemy.hp -= self.damage
        player.hp += self.heal
        player.mana += self.mana_gain
        return "Used " + self.name

    def make_description(self):
        if self.type == CardType.ATTACK:
            return f"Damage: {self.damage}\n, Range: {self.range}\n, Mana Cost: {self.mana_cost}\n"
        elif self.type == CardType.HEAL:
            return f"Heal: {self.heal}\n, Mana Cost: {self.mana_cost}\n"
        elif self.type == CardType.MOVE:
            return f"Move Range: {self.range}\n"
