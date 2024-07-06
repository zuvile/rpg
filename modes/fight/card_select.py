from util.cursor import Cursor
from pyray import *
from entities.card import CardType
from modes.fight.grid import Grid
from enum import Enum


class PlayerAction(Enum):
    ATTACK = 1
    HEAL = 2
    MOVE = 3
    IDLE = 4


class CardSelect(Cursor):
    def __init__(self):
        super().__init__()
        self.current_card = None
        self.player = None
        self.enemy = None
        self.done = False
        self.card_played = False
        self.player_action: PlayerAction = PlayerAction.IDLE
        self.map_arr = [[0 for _ in range(19)] for _ in range(11)]
        self.game_state = None
        self.grid = Grid()

    def enter(self, game_state):
        self.player = game_state.player
        self.enemy = game_state.get_interactable()
        self.game_state = game_state

    def is_card_selected(self):
        return self.current_card is not None

    def play_card(self):
        card = self.player.deck.cards[self.cursor_index]
        if is_key_pressed(KEY_ENTER):
            self.current_card = card

    def draw(self):
        if self.card_played and not self.player.in_animation():
            self.done = True
            return

        self.draw_card_deck()
        # wait for animation to finish
        if self.card_played and self.player.in_animation():
            return

        if self.player_action == PlayerAction.MOVE:
            self.handle_moving()
        elif self.player_action == PlayerAction.HEAL:
            self.handle_healing()
        elif self.player_action == PlayerAction.ATTACK:
            self.handle_attacking()
        else:
            self.move_cursor_horizontal(len(self.player.deck.cards))
            self.play_card()
            self.draw_selected_card()

            if self.current_card is None:
                return

            if self.current_card.type == CardType.HEAL:
                self.player_action = PlayerAction.HEAL
            elif self.current_card.type == CardType.MOVE:
                self.player_action = PlayerAction.MOVE
            elif self.current_card.type == CardType.ATTACK:
                self.player_action = PlayerAction.ATTACK

    def handle_attacking(self):
        cursor_point = self.grid.draw_grid(self.player, self.enemy, self.current_card, self.game_state)
        if cursor_point is not None:
            pts = self.player.do_attack()
            self.enemy.apply_damage(pts)
            self.player_action = PlayerAction.IDLE
            self.card_played = True
            self.game_state.add_to_log("You did " + str(pts) + " DMG")

    def handle_healing(self):
        self.player.heal(self.current_card.heal)
        self.player_action = PlayerAction.IDLE
        self.card_played = True
        self.game_state.add_to_log("You healed:" + str(self.current_card.heal) + " HP")

    def handle_moving(self):
        cursor_point = self.grid.draw_grid(self.player, self.enemy, self.current_card, self.game_state)
        if cursor_point is not None:
            self.player.auto_move(cursor_point.x - self.player.rec.x, cursor_point.y - self.player.rec.y)
            self.player_action = PlayerAction.IDLE
            self.card_played = True
            self.game_state.add_to_log("You moved.")

    def exit_state(self):
        self.current_card = None
        self.card_played = False
        self.done = False

    def draw_card_deck(self):
        x = 32
        y = 10 * 32

        for index, card in enumerate(self.player.deck.cards):
            colour = RED
            if self.cursor_index == index:
                colour = GREEN
            draw_rectangle(x + 32, y, 64, 64, colour)
            draw_text(card.name, x + 32, y, 20, BLACK)
            x += 62

    def draw_selected_card(self):
        curr_card = self.player.deck.cards[self.cursor_index]
        draw_rectangle(19 * 32, 10 * 32, 128, 192, GRAY)
        draw_text(curr_card.name, 20 * 32, 10 * 32, 20, BLACK)
        draw_text(curr_card.description, 19 * 32, 11 * 32, 16, BLACK)
