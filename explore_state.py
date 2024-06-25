from game_state import GameState
from pyray import *
from enemy import Enemy
from wall import Wall
from player import Player


class ExploreState(GameState):
    map = {
        'walls': [],
        'enemies': []
    }

    def __init__(self):
        self.add_walls()
        self.add_enemies()

    def add_walls(self):
        y = 0
        lines = open('assets/tiled_map_trees.csv', 'r').readlines()
        for line in lines:
            x = 0
            for char in line.split(','):
                if char != '-1':
                    self.map['walls'].append(Wall(x * 32, y * 32))
                x += 1
            y += 1

    def add_enemies(self):
        self.map['enemies'].append(Enemy(5 * 32, 5 * 32))

    def draw(self, player: Player):
        texture = load_texture('assets/tiled_map.png')
        draw_texture(texture, 0, 0, WHITE)
        player.draw()
        for wall in self.map['walls']:
            wall.draw()
        for enemy in self.map['enemies']:
            enemy.draw()
        action = player.move(self.map)

        return action
