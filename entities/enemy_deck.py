from util.sounds import play_sound
import random
import copy
from util.deck import update_deck, after_battle


class EnemyDeck:
    def __init__(self, pile):
        random.shuffle(pile)
        self.pile = pile
        self.maximum_hand_size = 3
        self.current_card = None
        self.hand = self.pile[0:4]
        self.pile = self.pile[4:]
        self.discard_pile = []
        self.trash_pile = []

    def play_card(self, card):
        self.current_card = card
        self.current_card.play()
        play_sound("play_card.wav")

    def finish_turn(self):
        if self.current_card.exhaust:
            self.hand.remove(self.current_card)
        self.discard_pile = copy.copy(self.hand)
        self.hand = []
        self.current_card = None

    def finish_battle(self):
        after_battle(self)

    def buff_all_cards(self, buff_card):
        for card in self.hand:
            card.set_tmp_buff(buff_card.buff)

    def in_animation(self):
        moving_cards = [card for card in self.hand if not card.animations_finished()]
        return len(moving_cards) > 0

    def clear_buffs(self):
        for card in self.hand:
            card.clear_buff()

    def update(self):
        update_deck(self)

    def shuffle(self, cards):
        random.shuffle(cards)

    def add_to_pile(self, cards):
        self.pile += cards
