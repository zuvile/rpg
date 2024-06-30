import pyray as rl
from entities.entity import Entity


class Wall(Entity):
    def __init__(self, x, y, size=32):
        super().__init__(x, y, size)

    def draw(self):
        rect = rl.Rectangle(self.rec.x, self.rec.y, self.rec.width, self.rec.height)
        rl.draw_rectangle_rec(rect, rl.BLANK)
