import pyray as rl
import random
from entities.entity import Entity
import textures as t


class Character(Entity):
    def __init__(self, texture, sub_texture, scale, x=0, y=0, size=32):
        super().__init__(x, y, size)
        self.attack = 10
        self.ac = 5
        self.hp = 20
        self.dead = False
        self.texture = texture
        self.scale = scale
        self.sub_texture = sub_texture

    def apply_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0

    def is_alive(self):
        return self.hp > 0

    def draw(self):
        t.load_texture(self.texture)
        texture = t.id_to_raylib(self.texture)
        destination = rl.Rectangle(self.rec.x, self.rec.y, self.sub_texture.width * self.scale, self.sub_texture.height * self.scale)
        origin = rl.Vector2(0, 0)
        rotation = 0.0
        sub_texture = rl.Rectangle(self.sub_texture.x, self.sub_texture.y, self.sub_texture.width, self.sub_texture.height)
        rl.draw_texture_pro(texture, sub_texture, destination, origin, rotation, rl.WHITE)

    def do_attack(self):
        return random.randint(0, self.attack)

    def add_health(self, health):
        self.hp += health
        if self.hp > 30:
            self.hp = 30
