from util.path_finding import get_distance
from entities.card import CardType

#todo refactor to always use tuples
def pick_card(deck, attacker_pos, defender_pos):
    #pick highest possible damage card
    attacker_pos = tuple([attacker_pos.x, attacker_pos.y])
    defender_pos = tuple([defender_pos.x, defender_pos.y])

    distance = get_distance(attacker_pos, defender_pos)
    best_card = None

    for card in deck:
        if card.type == CardType.ATTACK and card.get_range() >= distance:
            if best_card is None:
                best_card = card
            elif card.get_damage() > best_card.get_damage():
                best_card = card
    # if no damage is possible, try to dash and slash
    if best_card is None:
        for card in deck:
            if card.type == CardType.DASH_AND_SLASH and card.get_range() < distance:
                if best_card is None:
                    best_card = card
                elif card.get_range() < best_card.get_range():
                    best_card = card

    #if no slash and dash available, simply move
    if best_card is None:
        for card in deck:
            if card.type == CardType.MOVE:
                if best_card is None:
                    best_card = card
                elif card.get_range() > best_card.get_range():
                    best_card = card

    return best_card
