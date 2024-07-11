from util.cursor import Cursor
from pyray import *
from entities.card import CardType
from modes.fight.grid import Grid

class PlayerTurn(Cursor):
    def __init__(self):
        super().__init__()
        self.current_card = None
        self.player = None
        self.enemy = None
        self.done = False
        self.card_played = False
        self.game_state = None
        self.grid = Grid()
        self.has_moved = False

        self.action_handlers = {
            CardType.ATTACK: self.handle_attacking,
            CardType.HEAL: self.handle_healing,
            CardType.MOVE: self.handle_moving,
            CardType.BUFF: self.handle_buffing,
            CardType.DASH_AND_SLASH: self.handle_dash_and_slash,
        }

    def enter(self, game_state):
        self.player = game_state.player
        self.enemy = game_state.get_interactable()
        self.game_state = game_state

    def play_card(self):
        card = self.player.deck.cards[self.cursor_index]
        if is_key_pressed(KEY_ENTER):
            self.current_card = card

    def draw(self):
        if self.card_played and not self.player.in_animation() and not self.player.deck.in_animation():
            self.done = True
            return
        if not self.enemy.in_animation():
            self.player.deck.draw_card_deck(self.cursor_index)

        #wait for animations to finish
        if self.player.in_animation() or self.player.deck.in_animation():
            return
        if self.current_card is None:
            self.move_cursor_horizontal(len(self.player.deck.cards))
            self.draw_selected_card()
            self.play_card()
        else:
            self.action_handlers[self.current_card.type]()

    #this is not done using a card, fix this
    def handle_attacking(self):
        cursor_point = self.grid.select_square(self.player, self.enemy, self.current_card, self.game_state)
        self.handle_cancel()
        if cursor_point is not None:
            self.player.do_attack()
            pts = self.current_card.get_damage()
            self.enemy.apply_damage(pts)
            self.card_played = True
            self.game_state.add_to_log("You did " + str(pts) + " DMG")
            self.current_card = None

    def handle_healing(self):
        self.handle_cancel()
        self.player.heal(self.current_card.get_heal())
        self.card_played = True
        self.game_state.add_to_log("You healed:" + str(self.current_card.get_heal()) + " HP")
        self.current_card = None

    def handle_dash_and_slash(self):
        if self.has_moved:
            self.player.do_attack()
            pts = self.current_card.get_damage()
            self.enemy.apply_damage(pts)
            self.card_played = True
            self.game_state.add_to_log("You did " + str(pts) + " DMG")
            self.current_card = None
            self.has_moved = False
        else:
            cursor_point = self.grid.select_square(self.player, self.enemy, self.current_card, self.game_state)
            self.handle_cancel()
            if cursor_point is not None:
                path = self.grid.find_path(self.player, cursor_point)
                self.player.auto_move(path)
                self.has_moved = True

    def handle_moving(self):
        cursor_point = self.grid.select_square(self.player, self.enemy, self.current_card, self.game_state)
        self.handle_cancel()
        if cursor_point is not None:
            path = self.grid.find_path(self.player, cursor_point)
            self.player.auto_move(path)
            self.card_played = True
            self.current_card = None
            self.game_state.add_to_log("You moved.")

    def handle_buffing(self):
        self.player.deck.buff_all_cards(self.current_card)
        self.card_played = True
        self.game_state.add_to_log("Buffed: " + str(self.current_card.buff))
        self.current_card = None

    def exit_state(self):
        self.card_played = False
        self.done = False

    def draw_selected_card(self):
        curr_card = self.player.deck.cards[self.cursor_index]
        draw_rectangle(19 * 32, 10 * 32, 128, 192, GRAY)
        draw_text(curr_card.name, 20 * 32, 10 * 32, 20, BLACK)
        draw_text(curr_card.get_description(), 19 * 32, 11 * 32, 16, BLACK)

    def handle_cancel(self):
        if is_key_pressed(KEY_ESCAPE):
            self.current_card = None
            return