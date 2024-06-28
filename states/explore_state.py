from states.game_state import GameState
from pyray import *
from entities.player import Player
from actions import *


class ExploreState(GameState):
    def __init__(self):
        super().__init__()
        self.texture = load_texture('assets/tiled_map.png')

    def draw(self, player: Player, map):
        if is_key_pressed(KEY_M):
            return Actions.IN_GAME_MENU

        map.clear_dead()
        draw_texture(self.texture, 0, 0, WHITE)
        player.draw()
        for wall in map.walls:
            wall.draw()
        for enemy in map.enemies:
            enemy.draw()
        for friend in map.friends:
            friend.draw()

        action = player.move(map)

        return action
