from entities.card import Card, CardType
from pyray import *

class PlayerDeck:
    def __init__(self):
        self.maximum_hand_size = 6
        self.is_flashing = False
        self.picked_card = None
        self.flash_duration = 0
        self.cards = [
            Card('Strike', CardType.ATTACK, 10, 0, 2),
            Card('Strike', CardType.ATTACK, 10, 0, 2),
            Card('Heal', CardType.HEAL, 0, 10, 0,),
            Card('Buff', CardType.BUFF, 0, 0, 0),
        ]

    def buff_all_cards(self, buff_card):
        self.is_flashing = True
        self.flash_duration = 120
        for card in self.cards:
            card.set_tmp_buff(buff_card.buff)

    def draw_card_deck(self, cursor_index):
        screen_width = 1000
        card_width = 128
        spacing = 0
        total_cards_width = len(self.cards) * (card_width + spacing) - spacing
        start_x = (screen_width - total_cards_width) // 2

        if self.flash_duration > 0:
            self.flash_duration -= 1
        if self.flash_duration == 0:
            self.is_flashing = False
        x = start_x
        y = 14 * 32
        flash_color = WHITE if self.flash_duration % 20 < 10 else RED

        for index, card in enumerate(self.cards):
            colour = flash_color if self.flash_duration > 0 else RED
            card.color = colour
            if cursor_index == index:
                card.draw(x + 32, y - 32)
            else:
                card.x, card.y = x + 32,  y
                card.draw(x + 32,  y)
            x += card_width + spacing

    def in_animation(self):
        moving_cards = [card for card in self.cards if card.is_moving]
        return self.is_flashing or len(moving_cards) > 0

    def clear_buffs(self):
        for card in self.cards:
            card.clear_buff()
