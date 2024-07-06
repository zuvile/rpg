from modes.game_mode import GameMode
from pyray import *
from util.cursor import Cursor
from modes.fight_state_manager import FightStateManager


class FightMode(GameMode, Cursor):
    def __init__(self):
        super().__init__()
        self.fight_state_manager = FightStateManager()
        self.texture = load_texture('assets/maps/fight_map.png')
        self.player_turn = True
        self.start_of_fight = True

    def draw(self, game_state):
        if not game_state.is_layer_top(self):
            return

        self.draw_ui(game_state)
        if self.start_of_fight:
            self.setup(game_state)
            self.start_of_fight = False
        if not game_state.player.is_alive():
            self.handle_loss(game_state)
        if not game_state.get_interactable().is_alive():
            self.handle_win(game_state)

        if self.player_turn:
            self.fight_state_manager.set_state('card_select', game_state)
        else:
            self.fight_state_manager.set_state('enemy_turn', game_state)

        self.fight_state_manager.draw()

        if self.fight_state_manager.current_state_done():
            self.player_turn = not self.player_turn

    def handle_loss(self, game_state):
        self.handle_end_of_fight(game_state)

    def handle_win(self, game_state):
        self.handle_end_of_fight(game_state)

    def handle_end_of_fight(self, game_state):
        game_state.pop_render_layer()
        return

    def draw_ui(self, game_state):
        player = game_state.player
        enemy = game_state.get_interactable()
        draw_rectangle(0, 0, 800, 480, WHITE)
        draw_texture(self.texture, 0, 0, WHITE)
        player.draw()
        enemy.draw()
        draw_rectangle(19*32, 0, 10*32, 10*32, WHITE)
        draw_text("HP: " + str(player.hp), 20*32, 1*32, 16, BLACK)
        draw_text("Mana: " + str(player.mana), 20*32, 3*32, 16, BLACK)
        draw_text("Enemy HP: " + str(enemy.hp), 20*32, 2*32, 16, BLACK)
        log = game_state.get_log()
        for i in range(len(log)):
            draw_text(log[i], 19*32, (5+i)*32, 16, BLACK)

    def setup(self, game_state):
        player = game_state.player
        enemy = game_state.get_interactable()
        nearest_player_x = round(player.rec.x / 32) * 32
        nearest_player_y = round(player.rec.y / 32) * 32
        player.rec.x = nearest_player_x
        player.rec.y = nearest_player_y
        nearest_enemy_x = round(enemy.rec.x / 32) * 32
        nearest_enemy_y = round(enemy.rec.y / 32) * 32
        enemy.rec.x = nearest_enemy_x
        enemy.rec.y = nearest_enemy_y
