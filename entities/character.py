from entities.entity import Entity
import pyray as rl
from util import textures as t
from maps.map import MapType
import math

class Character(Entity):
    def __init__(self, texture, sub_texture, scale, deck, current_map, hp, x, y, size=32):
        super().__init__(x, y, size)
        self.hp = hp
        self.dead = False
        self.texture = texture
        self.scale = scale
        self.sub_texture = sub_texture
        self.max_hp = hp
        self.is_in_fight = False
        self.deck = deck
        self.current_map: MapType = current_map
        self.is_healing = False
        self.is_attacking = False
        self.is_healing = False
        self.is_attacking = False
        self.heal_animation_start_time = 0
        self.move_animation_start_time = 0
        self.attack_animation_start_time = 0

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
        destination = rl.Rectangle(self.rec.x, self.rec.y, self.sub_texture.width * self.scale,
                                   self.sub_texture.height * self.scale)
        origin = rl.Vector2(0, 0)
        rotation = 0.0
        sub_texture = rl.Rectangle(self.sub_texture.x, self.sub_texture.y, self.sub_texture.width,
                                   self.sub_texture.height)
        rl.draw_texture_pro(texture, sub_texture, destination, origin, rotation, color)

    def draw_in_battle(self):
        draw_color = rl.WHITE
        if self.is_in_fight:
            self.draw_health_bar(rl.GREEN)
            draw_color = rl.WHITE
            if self.is_healing:
                draw_color = rl.GREEN
                if rl.get_time() - self.heal_animation_start_time > 1:
                    self.is_healing = False
                    draw_color = rl.WHITE
            if self.is_attacking:
                if rl.get_time() - self.attack_animation_start_time > 1:
                    self.is_attacking = False
                    self.move_away_from_enemy()
                    draw_color = rl.WHITE
                    t.load_texture(self.texture)
        texture = t.id_to_raylib(self.texture)
        destination = rl.Rectangle(self.rec.x, self.rec.y, self.sub_texture.width * 4, self.sub_texture.height * 4)
        origin = rl.Vector2(0, 0)
        rotation = 0.0
        sub_texture = rl.Rectangle(self.sub_texture.x, self.sub_texture.y, self.sub_texture.width,
                                   self.sub_texture.height)
        rl.draw_texture_pro(texture, sub_texture, destination, origin, rotation, draw_color)

    def set_map(self, map: MapType):
        self.current_map = map

    def draw_health_bar(self, color):
        border_thickness = 1
        hp = math.ceil(128 / self.max_hp * self.hp)
        x = int(self.rec.x) - border_thickness
        y = int(self.rec.y) - 8 - border_thickness
        width = 128 + border_thickness * 2
        height = 8 + border_thickness * 2
        rl.draw_rectangle(x, y, width, height, rl.BLACK)
        rl.draw_rectangle(x + border_thickness, y + border_thickness, 32, 8, rl.WHITE)
        rl.draw_rectangle(x + border_thickness, y + border_thickness, hp, 8, color)

    def in_animation(self):
        return self.is_attacking or self.is_healing

    def do_attack(self):
        self.is_attacking = True
        self.move_towards_enemy()
        self.attack_animation_start_time = rl.get_time()

    def __repr__(self):
        return f"Character({self.rec.x}, {self.rec.y})"

    def move_towards_enemy(self):
        self.rec.x = self.rec.x - 96

    def move_away_from_enemy(self):
        self.rec.x = self.rec.x + 96
