from entities.card import Card, CardType
from pyray import *

class Deck:
    def __init__(self):
        self.is_flashing = False
        self.flash_duration = 0
        self.cards = [
            Card('Strike', CardType.ATTACK, 10, 0, 2, 0),
            Card('Heal', CardType.HEAL, 0, 10, 0, 0),
            Card('Move', CardType.MOVE, 0, 0, 2, 0),
            Card('Buff', CardType.BUFF, 0, 0, 0, 1),
        ]

    def buff_all_cards(self, buff_card):
        self.is_flashing = True
        self.flash_duration = 120
        for card in self.cards:
            card.set_tmp_buff(buff_card.buff)

    def draw_card_deck(self, cursor_index):
        if self.flash_duration > 0:
            self.flash_duration -= 1
        if self.flash_duration == 0:
            self.is_flashing = False
        x = 32
        y = 10 * 32
        flash_color = WHITE if self.flash_duration % 20 < 10 else RED

        for index, card in enumerate(self.cards):
            colour = flash_color if self.flash_duration > 0 else RED
            if cursor_index == index:
                colour = GREEN if self.flash_duration <= 0 else flash_color
            draw_rectangle(x + 32, y, 64, 64, colour)
            draw_text(card.name, x + 32, y, 20, BLACK)
            x += 62

    def in_animation(self):
        return self.is_flashing

    def clear_buffs(self):
        for card in self.cards:
            card.clear_buff()
