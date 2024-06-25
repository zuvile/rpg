from enemy import Enemy
from wall import Wall

class Map():
    enemies = []
    walls = []
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
                    self.walls.append(Wall(x * 32, y * 32))
                x += 1
            y += 1

    def add_enemies(self):
        self.enemies.append(Enemy(5 * 32, 5 * 32))

    def clear_dead(self):
        for enemy in self.enemies:
            if not enemy.is_alive():
                self.enemies.remove(enemy)