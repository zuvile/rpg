from modes.game_mode import GameMode
from pyray import *
from actions import *
from util.textures import id_to_raylib
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class ExploreMode(GameMode):
    def __init__(self):
        super().__init__()

    def draw(self, game_state):
        texture = game_state.current_map.texture
        raylib_texture = id_to_raylib(texture)
        draw_rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, BLACK)

        game_state.camera.begin()

        if is_key_pressed(KEY_M):
            return Actions.IN_GAME_MENU
        map = game_state.current_map
        player = game_state.player
        game_state.camera.set_target(Vector2(game_state.player.rec.x, game_state.player.rec.y))
        map.clear_dead()
        draw_texture(raylib_texture, 0, 0, WHITE)
        player.draw()
        for wall in map.walls:
            wall.draw()
        for enemy in map.enemies:
            enemy.draw()
        for friend in map.friends:
            friend.draw()
        if game_state.is_layer_top(self):
            player.move(game_state)
            print(f'{player.rec.x, player.rec.y}')
        game_state.camera.end()

