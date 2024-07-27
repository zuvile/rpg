from util.path_finding import get_distance
from entities.card import CardType

#todo refactor to always use tuples
def pick_card(deck, attacker_pos, defender_pos):
    best_card = None

    #tmp for testing purposes
    for card in deck:
        if card.type == CardType.ADD_TO_ENEMY_PILE:
            return card
        if card.type == CardType.ATTACK:
            if best_card is None:
                best_card = card
            elif card.get_damage() > best_card.get_damage():
                best_card = card

    return best_card
