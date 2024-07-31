def update_deck(deck):
    if len(deck.pile) < deck.maximum_hand_size:
        deck.pile += deck.discard_pile
    deck.shuffle(deck.pile)
    while len(deck.hand) < deck.maximum_hand_size and len(deck.pile) > 0:
        deck.hand.append(deck.pile.pop(0))