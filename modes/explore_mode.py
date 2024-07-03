from modes.game_mode import GameMode
from pyray import *
from actions import *


class ExploreMode(GameMode):
    def __init__(self):
        super().__init__()
        self.texture = load_texture('assets/tiled_map.png')

    def draw(self, game_state):
        if is_key_pressed(KEY_M):
            return Actions.IN_GAME_MENU
        map = game_state.map
        player = game_state.player
        map.clear_dead()
        draw_texture(self.texture, 0, 0, WHITE)
        player.draw()
        for wall in map.walls:
            wall.draw()
        for enemy in map.enemies:
            enemy.draw()
        for friend in map.friends:
            friend.draw()
        if game_state.is_layer_top(self):
            player.move(game_state)

