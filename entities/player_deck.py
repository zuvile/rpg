from entities.card import Card, CardType
import pyray as rl
from util.sounds import play_sound
import random
import copy
from animation.card_animations import FlashAnimation

class PlayerDeck:
    def __init__(self):
        self.maximum_hand_size = 3
        self.current_card = None
        self.flash_animation = FlashAnimation()

        self.hand = [
            Card('Strike', CardType.ATTACK, 10, 0, 2),
            Card('Strike', CardType.ATTACK, 10, 0, 2),
            Card('Heal', CardType.HEAL, 0, 10, 0),
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

    def finish(self):
        self.discard_pile = copy.copy(self.hand)
        self.hand = []

    def buff_all_cards(self, buff_card):
        self.flash_animation.start(rl.get_time())
        for card in self.hand:
            card.set_tmp_buff(buff_card.buff)

    def draw_card_deck(self, cursor_index):
        screen_width = 1000
        card_width = 128
        spacing = 0
        total_cards_width = len(self.hand) * (card_width + spacing) - spacing
        start_x = (screen_width - total_cards_width) // 2

        x = start_x
        y = 14 * 32
        i = self.flash_animation.eval(rl.get_time())
        flash_color = rl.WHITE if i == 0 else rl.RED

        for index, card in enumerate(self.hand):
            card.color = flash_color
            if cursor_index == index:
                card.draw(x + 32, y - 32)
            else:
                card.x, card.y = x + 32,  y
                card.draw(x + 32,  y)
            x += card_width + spacing

    def in_animation(self):
        # moving_cards = [card for card in self.hand if card.is_moving]
        return not self.flash_animation.finished(rl.get_time())

    def clear_buffs(self):
        for card in self.hand:
            card.clear_buff()

    def update(self):
        self.shuffle(self.pile)
        while len(self.hand) < self.maximum_hand_size and len(self.pile) > 0:
            self.hand.append(self.pile.pop(0))

        if len(self.hand) < self.maximum_hand_size:
            self.shuffle(self.discard_pile)
            self.pile += self.discard_pile

    def shuffle(self, cards):
        random.shuffle(cards)

    def add_to_pile(self, cards):
        self.pile += cards
