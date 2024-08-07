from modes.game_mode import GameMode
from pyray import *
from util.cursor import Cursor
from util.sounds import play_sound
import copy
from modes.fight_state_manager import FightStateManager
from effects.effects import Effects
from config import SCREEN_WIDTH, SCREEN_HEIGHT


class FightMode(GameMode, Cursor):
    def __init__(self):
        super().__init__()
        self.fight_state_manager = FightStateManager()
        self.texture = load_texture('assets/maps/.png')
        self.player_turn = True
        self.start_of_fight = True
        self.old_player_coordinates = None
        self.old_enemy_coordinates = None
        self.effects = Effects()

    def draw(self, game_state):
        if not game_state.is_layer_top(self):
            return

        game_state.camera.begin_fight_cam()

        if not game_state.player.is_alive() or not game_state.get_interactable().is_alive():
            self.handle_end(game_state)
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

        end_mode_2d()

    def handle_end(self, game_state):
        if not self.all_animations_done:
            game_state.player.update()
            game_state.get_interactable().update()
            return

        game_state.player.deck.finish_battle()
        game_state.get_interactable().deck.finish_battle()

        if not game_state.player.is_alive():
            self.handle_loss(game_state)
        else:
            self.handle_win(game_state)

    def handle_loss(self, game_state):
        game_state.tint(RED)
        play_sound('debuff.wav')
        draw_rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, RED)
        draw_text("You loose!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 32, BLACK)
        if is_key_pressed(KEY_ENTER):
            self.handle_end_of_fight(game_state)
            if game_state.fight_from_dialogue:
                game_state.last_fight_won = False

    def handle_win(self, game_state):
        draw_rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE)
        draw_text("You win!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 32, BLACK)
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
        draw_rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, GRAY)
        draw_texture(self.texture, 0, 0, WHITE)
        log = game_state.get_log()
        # for i in range(len(log)):
        #     draw_text(log[i], 25 * 32, (5 + i) * 32, 16, BLACK)

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
        game_state.camera.begin()

        player.change_position(64, 160)
        enemy.change_position(SCREEN_WIDTH - 128, 160)
        enemy.is_in_fight = True
        player.is_in_fight = True

    def all_animations_done(self, game_state):
        player = game_state.player
        return (not game_state.player.in_animation()
                and not game_state.get_interactable().in_animation()
                and not player.deck.in_animation())
