from util.path_finding import get_distance
from entities.card import CardType

#todo refactor to always use tuples
def pick_card(deck, attacker_pos, defender_pos):
    best_card = None

    for card in deck:
        if card.type == CardType.ATTACK:
            if best_card is None:
                best_card = card
            elif card.get_damage() > best_card.get_damage():
                best_card = card

    return best_card
