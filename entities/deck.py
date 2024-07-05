from entities.card import Card, CardType


class Deck:
    def __init__(self):
        self.cards = [
            Card('Strike', CardType.ATTACK, 10, 0, 2, 1, 0),
            Card('Heal', CardType.HEAL, 0, 10, 0, 1, 0),
            Card('Move', CardType.MOVE, 0, 0, 2, 0, 0),
        ]
