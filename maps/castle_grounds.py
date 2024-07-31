from entities.enemies.monster_melee import MonsterMelee
from entities.wall import Wall
from maps.map import Map
from util.textures import load_texture
from maps.map import MapType


class CastleGrounds(Map):
    def __init__(self):
        self.enemies = []
        self.walls = []
        self.friends = []
        self.add_walls()
        self.add_enemies()
        self.width = 800
        self.height = 600
        self.texture = load_texture('assets/tiled_map.png')
        self.type = MapType.CASTLE_GROUNDS

    def update(self, characters):
        self.clear_dead()
        self.friends = [char for char in characters if char.current_map == self.type]

    def add_walls(self):
        y = 0
        lines = open('assets/tiled_map_trees.csv', 'r').readlines()
        for line in lines:
            x = 0
            for char in line.split(','):
                if char != '-1':
                    self.walls.append(Wall(x * 32, y * 32))
                x += 1
            y += 1

    def add_enemies(self):
        self.enemies.append(MonsterMelee(self, 3 * 32, 3 * 32))

    def clear_dead(self):
        self.enemies = [enemy for enemy in self.enemies if enemy.is_alive()]
