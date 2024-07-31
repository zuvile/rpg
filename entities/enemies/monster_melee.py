from entities.enemy import Enemy
from entities.card import Card, CardType
from entities.rectangle import Rectangle
from entities.enemy_deck import EnemyDeck


# basic monster that attacks from melee range
class MonsterMelee(Enemy):
    def __init__(self, current_map, x, y, hp=30):
        super().__init__(current_map, hp, x, y)
        self.texture = 'assets/monsters.png'
        self.sub_texture = Rectangle(0, 0, 32, 32)
        self.scale = 1
        self.animation_start_time = 0
        self.is_attacking = False
        self.deck = EnemyDeck(self.get_cards())

    def get_cards(self):
        card = Card('Bleeding', CardType.DEBUFF, 0, 2, None, 0, 0, True)
        deck = [
            Card('Attack', CardType.ATTACK, 3, 0, 1),
            Card('Claw', CardType.ADD_TO_ENEMY_PILE, 0, 0, 0, card, 2)
        ]

        return deck
