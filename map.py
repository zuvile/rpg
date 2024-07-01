from entities.enemy import Enemy
from entities.friendly import Friendly
from entities.wall import Wall

class Map():
    def __init__(self):
        self.enemies = []
        self.walls = []
        self.friends = []
        self.add_walls()
        self.add_enemies()
        self.add_friends()

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
        self.friends.append(Friendly('Cassius', 'assets/portraits/cassius_normal.png',  3 * 32, 6 * 32))
        self.friends.append(Friendly('Mother', 'assets/portraits/placeholder.png', 3 * 32, 8 * 32))
        self.friends.append(Friendly('Master', 'assets/portraits/placeholder.png', 3 * 32, 10 * 32))

    def add_enemies(self):
        self.enemies.append(Enemy(5 * 32, 5 * 32))

    def clear_dead(self):
        for enemy in self.enemies:
            if not enemy.is_alive():
                self.enemies.remove(enemy)

    def update(self):
        self.clear_dead()
