from modes.game_mode import GameMode
from pyray import *
from actions import *


class ExploreMode(GameMode):
    def __init__(self):
        super().__init__()
        self.texture = load_texture('assets/tiled_map.png')
        self.camera = Camera2D()
        self.camera.target = Vector2(0, 0)
        self.camera.offset = Vector2(get_screen_width() / 2, get_screen_height() / 2)
        self.camera.rotation = 0.0
        self.camera.zoom = 2.0


    def draw(self, game_state):
        draw_rectangle(0, 0, 1600, 1600, BLACK)
        begin_mode_2d(self.camera)
        if is_key_pressed(KEY_M):
            return Actions.IN_GAME_MENU
        map = game_state.map
        player = game_state.player
        self.camera.target = Vector2(game_state.player.rec.x, game_state.player.rec.y)
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
        end_mode_2d()

