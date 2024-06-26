from states.game_state import GameState
from pyray import *
from player import Player
from actions import *


class ExploreState(GameState):
    def __init__(self):
        super().__init__()

    def draw(self, player: Player, map):
        if is_key_down(KEY_M):
            return Actions.IN_GAME_MENU

        map.clear_dead()
        texture = load_texture('assets/tiled_map.png')
        draw_texture(texture, 0, 0, WHITE)
        player.draw()
        for wall in map.walls:
            wall.draw()
        for enemy in map.enemies:
            enemy.draw()
        for friend in map.friends:
            friend.draw()

        action = player.move(map)

        return action
