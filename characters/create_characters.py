from entities.friendly import Friendly
from entities.card import Card, CardType
from entities.rectangle import Rectangle
from maps.map import MapType


# todo on each character specify which map they're in
def create_characters():
    characters = [
        get_cassius(),
        get_master(),
        get_mom(),
    ]

    return characters


def get_cassius():
    deck = [
        Card('Attack', CardType.ATTACK, 30, 0, 5),
        # Card('Cull the weak', CardType.ATTACK,

    ]

    portrait = 'assets/portraits/cassius.png'
    texture = 'assets/rogues.png'
    sub_texture = Rectangle(32, 128, 32, 32)
    cassius = Friendly('Cassius', portrait, texture, sub_texture, MapType.CASTLE_GROUNDS, 100, 3 * 32, 6 * 32)
    cassius.set_deck(deck)

    return cassius


def get_master():
    portrait = 'assets/portraits/placeholder.png'
    texture = 'assets/rogues.png'
    sub_texture = Rectangle(32, 96, 32, 32)
    return Friendly('Master', portrait, texture, sub_texture, MapType.CASTLE_GROUNDS, 100, 4 * 32, 8 * 32)


def get_mom():
    portrait = 'assets/portraits/mother.png'
    texture = 'assets/rogues.png'
    sub_texture = Rectangle(0, 128, 32, 32)
    return Friendly('Mother', portrait, texture, sub_texture, MapType.CASTLE_GROUNDS, 10, 4 * 32, 8 * 32)
