class Spell:
    def __init__(self, name, damage, heal, mana_cost, mana_gain):
        self.name = name
        self.damage = damage
        self.heal = heal
        self.mana_cost = mana_cost
        self.mana_gain = mana_gain


def get_spells(magic_lvl):
    spells = []
    if magic_lvl >= 1:
        spells.append(Spell('HEAL', 0, 10, 5, 0))
        spells.append(Spell('RESTORE_MANA', 0, 0, 0, 5))

    return spells
