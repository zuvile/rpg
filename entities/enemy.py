from entities.character import Character
from entities.rectangle import Rectangle
import random
import pyray as rl

class Enemy(Character):
    def __init__(self, x=0, y=0):
        texture = 'assets/free_character_1-3.png'
        sub_texture = Rectangle(0, 0, 16, 16)
        scale = 2
        self.animation_start_time = 0
        self.is_attacking = False

        super().__init__(texture, sub_texture, scale, x, y)

    def do_attack(self):
        self.is_attacking = True
        self.animation_start_time = rl.get_time()

        return random.randint(0, self.attack)

    def draw(self, color=rl.WHITE):
        self.draw_health()
        if self.is_attacking:
            draw_color = rl.RED
            if rl.get_time() - self.animation_start_time > 1:
                self.is_attacking = False
        else:
            draw_color = rl.WHITE
        super().draw(draw_color)

    def in_animation(self):
        return self.is_attacking

    def draw_health(self):
        rl.draw_rectangle(self.rec.x, self.rec.y - 8, 32, 8, rl.WHITE)
        rl.draw_rectangle(self.rec.x, self.rec.y - 8, self.hp, 8, rl.RED)
