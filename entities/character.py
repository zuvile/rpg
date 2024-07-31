from entities.entity import Entity
import pyray as rl
from util import textures as t
from maps.map import MapType
import math
from enum import Enum
from entities.enemy_deck import EnemyDeck


class CharacterBattleStatus(Enum):
    IDLE = 0
    HEALING = 1
    ATTACKING = 2
    TAKING_DAMAGE = 3
    BUFFING = 4


class Character(Entity):
    def __init__(self, texture, sub_texture, scale, current_map, hp, x, y, size=32):
        super().__init__(x, y, size)
        self.hp = hp
        self.dead = False
        self.texture = texture
        self.scale = scale
        self.sub_texture = sub_texture
        self.max_hp = hp
        self.is_in_fight = False
        self.deck = None
        self.current_map: MapType = current_map
        self.animation_start_time = 0
        self.status = CharacterBattleStatus.IDLE
        self.moved = False

    def set_deck(self, cards):
        self.deck = EnemyDeck(cards)

    def set_status(self, status: CharacterBattleStatus):
        self.status = status

    def apply_damage(self, damage):
        self.animation_start_time = rl.get_time()
        self.status = CharacterBattleStatus.TAKING_DAMAGE
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0

    def is_alive(self):
        return self.hp > 0

    def add_health(self, health):
        self.animation_start_time = rl.get_time()
        self.status = CharacterBattleStatus.HEALING
        self.hp += health
        if health + self.hp > self.max_hp:
            self.hp = self.max_hp

    def draw(self, color=rl.WHITE):
        self.update()
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
        draw_color = self.get_draw_color()
        if self.is_in_fight:
            self.draw_health_bar(rl.GREEN)

        texture = t.id_to_raylib(self.texture)
        destination = rl.Rectangle(self.rec.x, self.rec.y, self.sub_texture.width * 2, self.sub_texture.height * 2)
        origin = rl.Vector2(0, 0)
        rotation = 0.0
        sub_texture = rl.Rectangle(self.sub_texture.x, self.sub_texture.y, self.sub_texture.width,
                                   self.sub_texture.height)
        rl.draw_texture_pro(texture, sub_texture, destination, origin, rotation, draw_color)

    def get_draw_color(self):
        colour = rl.WHITE
        if self.status == CharacterBattleStatus.HEALING:
            return rl.GREEN
        if self.status == CharacterBattleStatus.TAKING_DAMAGE:
            return rl.RED
        if self.status == CharacterBattleStatus.ATTACKING:
            return rl.BLUE

        return colour

    def update(self):
        if rl.get_time() - self.animation_start_time > 2:
            self.status = CharacterBattleStatus.IDLE

    def set_map(self, map: MapType):
        self.current_map = map

    def draw_health_bar(self, color):
        border_thickness = 1
        hp = math.ceil(64 / self.max_hp * self.hp)
        x = int(self.rec.x) - border_thickness
        y = int(self.rec.y) - 8 - border_thickness
        width = 64 + border_thickness * 2
        height = 8 + border_thickness * 2
        rl.draw_rectangle(x, y, width, height, rl.BLACK)
        rl.draw_rectangle(x + border_thickness, y + border_thickness, 64, 8, rl.WHITE)
        rl.draw_rectangle(x + border_thickness, y + border_thickness, hp, 8, color)

    def in_animation(self):
        return self.status != CharacterBattleStatus.IDLE

    def start_attack(self):
        self.move_towards_enemy()
        self.moved = True
        self.status = CharacterBattleStatus.ATTACKING
        self.animation_start_time = rl.get_time()

    def start_buffing(self):
        self.status = CharacterBattleStatus.BUFFING
        self.animation_start_time = rl.get_time()

    def end_attack(self):
        if self.moved:
            self.move_away_from_enemy()
            self.moved = False
        self.deck.finish_turn()

    def __repr__(self):
        return f"Character({self.rec.x}, {self.rec.y})"

    def move_towards_enemy(self):
        self.rec.x = self.rec.x - 96

    def move_away_from_enemy(self):
        self.rec.x = self.rec.x + 96
