from entities.character import Character
from entities.rectangle import Rectangle
import random
import pyray as rl

class Enemy(Character):
    def __init__(self, x=0, y=0):
        texture = 'assets/free_character_1-3.png'
        sub_texture = Rectangle(0, 0, 16, 16)
        scale = 2
        self.in_animation = False
        self.animation_start_time = 0
        self.is_attacking = False

        super().__init__(texture, sub_texture, scale, x, y)

    def do_attack(self):
        self.in_animation = True
        self.is_attacking = True
        self.animation_start_time = rl.get_time()

        return random.randint(0, self.attack)

    def draw(self, color=rl.WHITE):
        if self.is_attacking:
            draw_color = rl.RED
            if rl.get_time() - self.animation_start_time > 1:
                self.is_attacking = False
                self.in_animation = False
        else:
            draw_color = rl.WHITE
        super().draw(draw_color)
