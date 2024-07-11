from entities.enemies.monster_melee import MonsterMelee
from entities.friendly import Friendly
from entities.wall import Wall
from entities.rectangle import Rectangle

class Map():
    def __init__(self):
        self.enemies = []
        self.walls = []
        self.friends = []
        self.add_walls()
        self.add_enemies()
        self.add_friends()
        self.width = 800
        self.height = 600
        self.movable_area = Rectangle(0, 0, self.width, self.height)

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

    def add_friends(self):
        self.friends.append(Friendly('Cassius', 'assets/portraits/cassius_normal.png',  3 * 32, 6 * 32, 100, 100, 100, 100, 100))
        self.friends.append(Friendly('Mother', 'assets/portraits/placeholder.png', -1 * 32, -1 * 32))
        self.friends.append(Friendly('Master', 'assets/portraits/placeholder.png', -1 * 32, -1 * 32))

    def add_enemies(self):
        self.enemies.append(MonsterMelee(5 * 32, 5 * 32))

    def clear_dead(self):
        for enemy in self.enemies:
            if not enemy.is_alive():
                self.enemies.remove(enemy)

    def update(self):
        self.clear_dead()

    def set_movable_area(self, x, y, width, height):
        self.movable_area = Rectangle(x, y, width, height)
