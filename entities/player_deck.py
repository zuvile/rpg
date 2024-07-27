from entities.card import Card, CardType
import pyray as rl
from util.sounds import play_sound
import random

class PlayerDeck:
    def __init__(self):
        self.maximum_hand_size = 3
        self.is_flashing = False
        self.picked_card = None
        self.flash_duration = 0
        self.current_card = None
        self.hand = [
            Card('Strike', CardType.ATTACK, 10, 0, 2),
            Card('Strike', CardType.ATTACK, 10, 0, 2),
            Card('Heal', CardType.HEAL, 0, 10, 0,),
            Card('Buff', CardType.BUFF, 0, 0, 0),
        ]

        self.remove_from_hand = []

        self.discard_pile = []
        self.trash_pile = []
        self.pile = [
        ]

    def play_card(self, index):
        card = self.hand[index]
        card.play()
        play_sound("play_card.wav")
        self.remove_from_hand.append(index)

    def buff_all_cards(self, buff_card):
        self.is_flashing = True
        self.flash_duration = 120
        for card in self.hand:
            card.set_tmp_buff(buff_card.buff)

    def draw_card_deck(self, cursor_index):
        screen_width = 1000
        card_width = 128
        spacing = 0
        total_cards_width = len(self.hand) * (card_width + spacing) - spacing
        start_x = (screen_width - total_cards_width) // 2

        if self.flash_duration > 0:
            self.flash_duration -= 1
        if self.flash_duration == 0:
            self.is_flashing = False
        x = start_x
        y = 14 * 32
        flash_color = rl.WHITE if self.flash_duration % 20 < 10 else rl.RED

        for index, card in enumerate(self.hand):
            colour = flash_color if self.flash_duration > 0 else rl.RED
            card.color = colour
            if cursor_index == index:
                card.draw(x + 32, y - 32)
            else:
                card.x, card.y = x + 32,  y
                card.draw(x + 32,  y)
            x += card_width + spacing

    def in_animation(self):
        moving_cards = [card for card in self.hand if card.is_moving]
        return self.is_flashing or len(moving_cards) > 0

    def clear_buffs(self):
        for card in self.hand:
            card.clear_buff()

    def update(self):
        for index in self.remove_from_hand:
            self.discard_pile.append(self.hand[index])
            self.hand.remove(self.hand[index])
        self.remove_from_hand = []

        while len(self.hand) < self.maximum_hand_size and len(self.pile) > 0:
            self.hand.append(self.pile.pop(0))

        if len(self.hand) < self.maximum_hand_size:
            self.discard_pile = self.shuffle(self.discard_pile)
            self.pile += self.discard_pile

    def shuffle(self, cards):
        random.shuffle(cards)

        return cards
