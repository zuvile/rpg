from pyray import *

from object import Object

class Character(Object):
    def __init__(self, x=0, y=0, size=32, color=RED):
        super().__init__(x, y, size)
        self.color = color
        self.texture = load_texture('assets/free_character_1-3.png')
        self.sub_texture = Rectangle(48, 0, 15, 20)
        self.scale = 2

    def draw(self):
        destination = Rectangle(self.rec.x, self.rec.y, self.sub_texture.width * self.scale, self.sub_texture.height * self.scale)
        origin = Vector2(0, 0)
        rotation = 0.0
        draw_texture_pro(self.texture, self.sub_texture, destination, origin, rotation, WHITE)