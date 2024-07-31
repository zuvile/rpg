from entities.card import CardType


def pick_card(deck):
    best_card = deck.hand[0]

    for card in deck.hand:
        if card.type == CardType.ADD_TO_ENEMY_PILE:
            return card
        if card.type == CardType.ATTACK:
            if best_card is None:
                best_card = card
            elif card.get_damage() > best_card.get_damage():
                best_card = card

    return best_card
