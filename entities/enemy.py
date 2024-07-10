from entities.character import Character
from entities.rectangle import Rectangle
import random
import pyray as rl
from entities.character_elements import draw_health_bar
class Enemy(Character):
    def __init__(self, x=0, y=0):
        texture = 'assets/monsters.png'
        sub_texture = Rectangle(0, 0, 32, 32)
        scale = 1
        self.animation_start_time = 0
        self.is_attacking = False

        super().__init__(texture, sub_texture, scale, x, y)

    def do_attack(self):
        self.is_attacking = True
        self.animation_start_time = rl.get_time()

        return random.randint(0, self.attack)

    def draw(self, color=rl.WHITE):
        if self.is_in_fight:
            draw_health_bar(rl.RED, self)
        if self.is_attacking:
            draw_color = rl.RED
            if rl.get_time() - self.animation_start_time > 1:
                self.is_attacking = False
        else:
            draw_color = rl.WHITE
        super().draw(draw_color)

    def in_animation(self):
        return self.is_attacking

