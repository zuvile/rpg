from entities.entity import Entity
import pyray as rl
from util import textures as t
from maps.map import MapType


class Character(Entity):
    def __init__(self, texture, sub_texture, scale, deck, current_map, x=0, y=0,  size=32, ac=5, hp=10):
        super().__init__(x, y, size)
        self.ac = ac
        self.hp = hp
        self.dead = False
        self.texture = texture
        self.scale = scale
        self.sub_texture = sub_texture
        self.max_hp = hp
        self.is_in_fight = False
        self.deck = deck
        self.current_map: MapType = current_map

    def apply_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0

    def is_alive(self):
        return self.hp > 0

    def add_health(self, health):
        self.hp += health
        if self.hp > 30:
            self.hp = 30

    def draw(self, color=rl.WHITE):
        t.load_texture(self.texture)
        texture = t.id_to_raylib(self.texture)
        destination = rl.Rectangle(self.rec.x, self.rec.y, self.sub_texture.width * self.scale, self.sub_texture.height * self.scale)
        origin = rl.Vector2(0, 0)
        rotation = 0.0
        sub_texture = rl.Rectangle(self.sub_texture.x, self.sub_texture.y, self.sub_texture.width, self.sub_texture.height)
        rl.draw_texture_pro(texture, sub_texture, destination, origin, rotation, color)

    def set_map(self, map: MapType):
        self.current_map = map
