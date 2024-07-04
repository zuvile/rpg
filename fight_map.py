from entities.rectangle import Rectangle

class FightMap():
    def __init__(self):
        self.enemies = []
        self.walls = []
        self.friends = []
        self.width = 18 * 32
        self.height = 10 * 32
        self.movable_area = Rectangle(0, 0, 0, 0)


    def add_enemy(self, enemy):
        self.enemies.append(enemy)

    def clear_dead(self):
        for enemy in self.enemies:
            if not enemy.is_alive():
                self.enemies.remove(enemy)

    def update(self):
        self.clear_dead()

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height

    def set_movable_area(self, x, y, width, height):
        self.movable_area = Rectangle(x, y, width, height)


