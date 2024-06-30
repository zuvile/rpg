import pyray as rl

class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


    def to_raylib(self):
        return rl.Rectangle(self.x, self.y, self.width, self.height)
