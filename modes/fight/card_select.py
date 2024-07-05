from cursor import Cursor
from pyray import *
from entities.card import CardType

class CardSelect(Cursor):
    def __init__(self):
        super().__init__()
        self.current_card = None
        self.player = None
        self.enemy = None
        self.done = False
        self.card_played = False

    def enter(self, game_state):
        self.player = game_state.player
        self.enemy = game_state.get_interactable()
        self.current_card = None

    def is_card_selected(self):
        return self.current_card is not None

    def play_card(self):
        card = self.player.deck.cards[self.cursor_index]
        if is_key_pressed(KEY_ENTER):
            self.current_card = card

    def draw(self):
        if self.card_played and not self.player.in_animation:
            self.done = True
            return

        self.move_cursor_horizontal(len(self.player.deck.cards))
        self.draw_card_deck()

        self.play_card()
        self.draw_selected_card()

        if self.current_card is None:
            return

        if self.current_card.type == CardType.HEAL:
            self.handle_heal_card()


    def handle_heal_card(self):
        self.player.heal(self.current_card.heal)
        self.card_played = True

    def exit_state(self):
        self.current_card = None
        self.card_played = False
        self.done = False

    def draw_card_deck(self):
        x = 32
        y = 10*32

        for index, card in enumerate(self.player.deck.cards):
            colour = RED
            if self.cursor_index == index:
                colour = GREEN
            draw_rectangle(x + 32, y, 64, 64, colour)
            draw_text(card.name, x + 32, y, 20, BLACK)
            x += 62

    def draw_selected_card(self):
        curr_card = self.player.deck.cards[self.cursor_index]
        draw_rectangle(19*32, 10*32, 128, 192, GRAY)
        draw_text(curr_card.name, 20*32, 10*32, 20, BLACK)
        draw_text(curr_card.description, 19*32, 11*32, 16, BLACK)
