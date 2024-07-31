import random

def update_deck(deck):
    if len(deck.pile) < deck.maximum_hand_size:
        deck.pile += deck.discard_pile
    deck.shuffle(deck.pile)
    while len(deck.hand) < deck.maximum_hand_size and len(deck.pile) > 0:
        deck.hand.append(deck.pile.pop(0))

def after_battle(deck):
    deck.pile += deck.hand + deck.discard_pile + deck.trash_pile
    deck.hand = []
    deck.discard_pile = []
    deck.trash_pile = []
    for card in deck.pile:
        if card.temp:
            deck.pile.remove(card)

    random.shuffle(deck.pile)
