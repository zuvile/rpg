from modes.game_mode import GameMode
from pyray import *
from util.cursor import Cursor
import copy
from modes.fight_state_manager import FightStateManager

class FightMode(GameMode, Cursor):
    def __init__(self):
        super().__init__()
        self.fight_state_manager = FightStateManager()
        self.texture = load_texture('assets/maps/.png')
        self.player_turn = True
        self.start_of_fight = True
        self.old_player_coordinates = None
        self.old_enemy_coordinates = None

    def draw(self, game_state):
        if not game_state.is_layer_top(self):
            return

        if not game_state.player.is_alive() and self.all_animations_done(game_state):
            self.handle_loss(game_state)
            return
        if not game_state.get_interactable().is_alive() and self.all_animations_done(game_state):
            self.handle_win(game_state)
            return

        self.draw_ui(game_state)
        self.draw_characters(game_state)

        if self.start_of_fight:
            self.setup(game_state)
            self.start_of_fight = False

        if self.player_turn:
            self.fight_state_manager.set_state('player_turn', game_state)
        else:
            self.fight_state_manager.set_state('enemy_turn', game_state)

        self.fight_state_manager.draw()

        if self.fight_state_manager.current_state_done():
            self.player_turn = not self.player_turn

    def handle_loss(self, game_state):
        draw_rectangle(0, 0, 1000, 600, WHITE)
        # Centering "You lose!" text
        draw_text("You lose!", 460, 300, 32, BLACK)  # Adjusted x-coordinate for centering
        if is_key_pressed(KEY_ENTER):
            self.handle_end_of_fight(game_state)
            if game_state.fight_from_dialogue:
                game_state.last_fight_won = False

    def handle_win(self, game_state):
        draw_rectangle(0, 0, 1000, 600, WHITE)
        # Centering "You win!" text
        draw_text("You win!", 460, 300, 32, BLACK)  # Adjusted x-coordinate for centering
        if is_key_pressed(KEY_ENTER):
            self.handle_end_of_fight(game_state)
            if game_state.fight_from_dialogue:
                game_state.last_fight_won = True

    def handle_end_of_fight(self, game_state):
        player = game_state.player
        enemy = game_state.get_interactable()
        player.is_in_fight = False
        enemy.is_in_fight = False
        player.rec = self.old_player_coordinates
        enemy.rec = self.old_enemy_coordinates
        game_state.pop_render_layer()
        return

    def draw_ui(self, game_state):
        draw_rectangle(0, 0, 1000, 600, GRAY)
        draw_texture(self.texture, 0, 0, WHITE)
        log = game_state.get_log()
        for i in range(len(log)):
            draw_text(log[i], 25*32, (5+i)*32, 16, BLACK)


    def draw_characters(self, game_state):
        player = game_state.player
        enemy = game_state.get_interactable()
        player.draw_in_battle()
        enemy.draw_in_battle()

    def setup(self, game_state):
        player = game_state.player
        enemy = game_state.get_interactable()
        self.old_player_coordinates = copy.copy(player.rec)
        self.old_enemy_coordinates = copy.copy(enemy.rec)

        player.change_position(128, 192)
        enemy.change_position(672, 192)
        enemy.is_in_fight = True
        player.is_in_fight = True


    def all_animations_done(self, game_state):
        return not game_state.player.in_animation() and not game_state.get_interactable().in_animation()
