from entities.enemies.monster_melee import MonsterMelee
from entities.friendly import Friendly
from entities.wall import Wall
from entities.rectangle import Rectangle
from characters.create_characters import create_characters
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
        chars = create_characters()
        for char in chars:
            self.friends.append(char)

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
