from entities.character import Character
from entities.rectangle import Rectangle
import random
import pyray as rl
from entities.character_elements import draw_health_bar


class Enemy(Character):
    def __init__(self, deck, x=0, y=0, hp=30, ):
        texture = 'assets/monsters.png'
        sub_texture = Rectangle(0, 0, 32, 32)
        scale = 1
        self.animation_start_time = 0
        self.is_attacking = False
        self.move_speed = 1.0
        self.last_move_time = 0
        self.path_index = 0
        self.is_walking = False
        self.path = []
        self.move_animation_start_time = 0
        self.attack_animation_start_time = 0

        #todo change this
        super().__init__(texture, sub_texture, scale, deck, x, y, 32, 5, hp)

    def play_card(self):
        self.is_attacking = True
        self.animation_start_time = rl.get_time()

        return random.randint(0, self.attack)

    def draw(self, color=rl.WHITE):
        if self.is_in_fight:
            draw_health_bar(rl.RED, self)

        draw_color = rl.WHITE

        if self.is_attacking:
            draw_color = rl.RED
            if rl.get_time() - self.attack_animation_start_time > 1:
                self.is_attacking = False
                draw_color = rl.WHITE
        if self.is_walking and rl.get_time() - self.last_move_time >= self.move_speed:
            draw_color = rl.BLUE
            if self.path_index < len(self.path):
                next_pos = self.path[self.path_index]
                self.rec.x = next_pos[0] * 32
                self.rec.y = next_pos[1] * 32
                self.path_index += 1
                self.last_move_time = rl.get_time()
            else:
                self.is_walking = False
        super().draw(draw_color)

    def in_animation(self):
        return self.is_attacking or self.is_walking

    def auto_move(self, path):
        self.is_walking = True
        self.path_index = 0
        self.move_animation_start_time = rl.get_time()
        self.last_move_time = rl.get_time()
        self.path = path

    def do_attack(self):
        self.is_attacking = True
        self.attack_animation_start_time = rl.get_time()
