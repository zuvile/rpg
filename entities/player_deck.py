from entities.card import Card, CardType, CardParams
import pyray as rl
from util.sounds import play_sound
import random
import copy
from animation.card_animations import FlashAnimation
from config import SCREEN_WIDTH, SCREEN_HEIGHT


class PlayerDeck:
    def __init__(self):
        self.maximum_hand_size = 3
        self.current_card = None
        self.flash_animation = FlashAnimation()

        self.hand = [
            Card('Strike', CardType.ATTACK, 10, 0, 2),
            Card('Strike', CardType.ATTACK, 10, 0, 2),
            Card('Heal', CardType.HEAL, 0, 10, 0),
        ]

        self.discard_pile = []
        self.trash_pile = []
        self.pile = [
            Card('Strike', CardType.ATTACK, 10, 0, 2),
            Card('Buff', CardType.BUFF, 0, 0, 0),
        ]

    def play_card(self, index):
        card = self.hand[index]
        card.play()
        print('anim')
        print(card.animations_finished())
        play_sound("play_card.wav")

    def finish(self):
        if self.current_card.exhaust:
            self.hand.remove(self.current_card)
        self.discard_pile = copy.copy(self.hand)
        self.hand = []
        self.current_card = None

    def buff_all_cards(self, buff_card):
        self.flash_animation.start(rl.get_time())
        for card in self.hand:
            card.set_tmp_buff(buff_card.buff)

    def draw_card_deck(self, cursor_index):
        spacing = 0
        total_cards_width = len(self.hand) * (CardParams.WIDTH.value + spacing) - spacing
        start_x = (SCREEN_WIDTH - total_cards_width) // 2

        x = start_x
        y = SCREEN_HEIGHT - 16
        i = self.flash_animation.eval(rl.get_time())
        flash_color = rl.WHITE if i == 0 else rl.RED

        for index, card in enumerate(self.hand):
            card.color = flash_color
            if cursor_index == index:
                card.draw(x + 32, y - 32)
            else:
                card.x, card.y = x + 32, y
                card.draw(x + 32, y)
            x += card.width + spacing

    def draw_discard(self):
        if len(self.discard_pile) > 0:
            x = CardParams.WIDTH.value
            y = SCREEN_HEIGHT - CardParams.WIDTH.value - 32
            rl.draw_text('DISCARD', x, y - 8, 8, rl.BLACK)
            rl.draw_rectangle(x, y, CardParams.WIDTH.value, CardParams.HEIGHT.value, rl.WHITE)
            rl.draw_text('items: ' + str(len(self.discard_pile)), x + 8, y + 8, 8, rl.BLACK)

    def draw_pile(self):
        if len(self.pile) > 0:
            x = SCREEN_WIDTH - CardParams.WIDTH.value - 32
            y = SCREEN_HEIGHT - CardParams.WIDTH.value - 32
            rl.draw_text('DRAW', x, y - 8, 8, rl.BLACK)
            rl.draw_rectangle(x, y, CardParams.WIDTH.value, CardParams.HEIGHT.value, rl.WHITE)
            rl.draw_text('items: ' + str(len(self.pile)), x + 8, y + 8, 8, rl.BLACK)

    def in_animation(self):
        moving_cards = [card for card in self.hand if not card.animations_finished()]
        return not self.flash_animation.finished(rl.get_time()) and len(moving_cards) > 0

    def clear_buffs(self):
        for card in self.hand:
            card.clear_buff()

    def update(self):
        if len(self.pile) < self.maximum_hand_size:
            self.pile += self.discard_pile
        self.shuffle(self.pile)
        while len(self.hand) < self.maximum_hand_size and len(self.pile) > 0:
            self.hand.append(self.pile.pop(0))

    def shuffle(self, cards):
        random.shuffle(cards)

    def add_to_pile(self, cards):
        self.pile += cards
