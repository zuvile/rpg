from entities.friendly import Friendly
from entities.card import Card, CardType
from entities.rectangle import Rectangle


def create_characters():
    characters = [
        get_cassius(),
        get_get_julius(),
        get_oswald(),
        get_master(),
        get_mom(),
    ]

    return characters


# archtype: dark and serious. Cards have powerful kill mechanics

def get_cassius():
    # some ideas for cards:
    # teleport card
    # kill card that insta kills all enemies with less than 10 hp
    #
    deck = [
        Card('Super Attack', CardType.ATTACK, 30, 0, 5, 0, False),
        Card('Dash and slash', CardType.DASH_AND_SLASH, 10, 0, 0, 0, True),
        # Card('Cull the weak', CardType.ATTACK,

    ]

    portrait = 'assets/portraits/cassius_normal.png'
    texture = 'assets/rogues.png'
    sub_texture = Rectangle(32, 128, 32, 32)
    return Friendly('Cassius', portrait, deck, texture, sub_texture, 3 * 32, 6 * 32, 100,
                    100)

# archtype: friendly and helpful. Cards have buffs and heals
def get_get_julius():
    deck = [
        Card('Heal', CardType.HEAL, 0, 10, 0, 0),
        Card('Buff', CardType.BUFF, 0, 0, 0, 1),
        Card('Move', CardType.MOVE, 0, 0, 2, 0),
        Card('Attack', CardType.ATTACK, 10, 0, 2, 0),
        Card('Dash and slash', CardType.DASH_AND_SLASH, 10, 0, 0, 0, True),
    ]

    portrait = 'assets/portraits/placeholder.png'
    texture = 'assets/rogues.png'
    sub_texture = Rectangle(32, 32, 32, 32)
    return Friendly('Julius', portrait, deck, texture, sub_texture, 6 * 32, 8 * 32, 100,
                    100)

# archtype: sarcastic and funny. cards have powers that charm and disorient enemeis
def get_oswald():
    deck = [
        # Card('Confuse', CardType.CONFUSE, 0, 0, 0, 0),
        # Card('Charm', CardType.CHARM, 0, 0, 0, 0),
        Card('Move', CardType.MOVE, 0, 0, 2, 0),
        Card('Attack', CardType.ATTACK, 10, 0, 2, 0),
        Card('Dash and slash', CardType.DASH_AND_SLASH, 10, 0, 0, 0, True),
    ]

    portrait = 'assets/portraits/placeholder.png'
    texture = 'assets/rogues.png'
    sub_texture = Rectangle(32, 128, 32, 32)
    return Friendly('Oswald', portrait, deck, texture, sub_texture, 4 * 32, 8 * 32, 100,
                    100)

def get_master():
    portrait = 'assets/portraits/placeholder.png'
    texture = 'assets/rogues.png'
    sub_texture = Rectangle(32, 96, 32, 32)
    return Friendly('Master', portrait, [], texture, sub_texture, 4 * 32, 8 * 32, 100,
                    100)

def get_mom():
    portrait = 'assets/portraits/placeholder.png'
    texture = 'assets/rogues.png'
    sub_texture = Rectangle(0, 128, 32, 32)
    return Friendly('Mom', portrait, [], texture, sub_texture, 4 * 32, 8 * 32, 100,
                    100)
