from entities.enemy import Enemy
from entities.card import Card, CardType
from entities.rectangle import Rectangle

#basic monster that attacks from melee range
class MonsterMelee(Enemy):
    def __init__(self, current_map, x=0, y=0, hp=30):
        super().__init__(current_map, x, y, hp)
        self.texture = 'assets/monsters.png'
        self.sub_texture = Rectangle(0, 0, 32, 32)
        self.scale = 1
        self.animation_start_time = 0
        self.is_attacking = False
        self.deck = [
            Card('Attack', CardType.ATTACK, 3, 0, 1, 0, 0)
        ]

