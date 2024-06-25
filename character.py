from pyray import *
import random

from object import Object

class Character(Object):
    attack = 10
    ac = 5
    hp = 20
    dead = False

    def __init__(self, texture, sub_texture, scale, x=0, y=0, size=32):
        super().__init__(x, y, size)
        self.texture = texture
        self.sub_texture = sub_texture
        self.scale = scale

    def apply_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0

    def is_alive(self):
        return self.hp > 0

    def draw(self):
        destination = Rectangle(self.rec.x, self.rec.y, self.sub_texture.width * self.scale, self.sub_texture.height * self.scale)
        origin = Vector2(0, 0)
        rotation = 0.0
        draw_texture_pro(self.texture, self.sub_texture, destination, origin, rotation, WHITE)

    def do_attack(self):
        return random.randint(0, self.attack)
