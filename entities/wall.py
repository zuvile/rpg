from pyray import *
from entities.entity import Entity


class Wall(Entity):
    def __init__(self, x, y, size=32):
        super().__init__(x, y, size)
    def draw(self):
        draw_rectangle_rec(self.rec, BLANK)
