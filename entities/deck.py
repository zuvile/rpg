from entities.card import Card

class Deck:
    def __init__(self):
        self.cards = [
            Card('Strike', 10, 0, 1, 1, 0),
            Card('Heal', 0, 10, 0, 1, 0)
        ]
