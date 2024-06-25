from pyray import *
from Object import Object


class Wall(Object):
    def __init__(self, x, y, size=32):
        super().__init__(x, y, size)
    def draw(self):
        rec = Rectangle(self.position.x, self.position.y, self.size, self.size)
        draw_rectangle_rec(rec, BLACK)