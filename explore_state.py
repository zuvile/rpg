from game_state import GameState
from pyray import *
from player import Player


class ExploreState(GameState):
    def draw(self, player: Player, map):
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
