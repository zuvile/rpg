from pyray import *

from object import Object

class Character(Object):
    attack = 10
    defence = 10
    def __init__(self, texture, sub_texture, scale, x=0, y=0, size=32):
        super().__init__(x, y, size)
        self.texture = texture
        self.sub_texture = sub_texture
        self.scale = scale

    def draw(self):
        destination = Rectangle(self.rec.x, self.rec.y, self.sub_texture.width * self.scale, self.sub_texture.height * self.scale)
        origin = Vector2(0, 0)
        rotation = 0.0
        draw_texture_pro(self.texture, self.sub_texture, destination, origin, rotation, WHITE)
