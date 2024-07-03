class Card:
    def __init__(self, name, damage, heal, range, mana_cost, mana_gain):
        self.name = name
        self.damage = damage
        self.heal = heal
        self.range = range
        self.mana_cost = mana_cost
        self.mana_gain = mana_gain

    def use(self, player, enemy):
        if player.mana < self.mana_cost:
            return "Not enough mana"
        player.mana -= self.mana_cost
        enemy.hp -= self.damage
        player.hp += self.heal
        player.mana += self.mana_gain
        return "Used " + self.name
