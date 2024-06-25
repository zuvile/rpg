from pyray import *
from object import Object


class Wall(Object):
    def __init__(self, x, y, size=32):
        super().__init__(x, y, size)
    def draw(self):
        draw_rectangle_rec(self.rec, BLANK)