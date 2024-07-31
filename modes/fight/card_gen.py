from entities.character import Character
from copy import deepcopy


def add_multi(card, amount, character: Character):
    cards = [deepcopy(card) for _ in range(amount)]
    character.deck.add_to_pile(cards)
