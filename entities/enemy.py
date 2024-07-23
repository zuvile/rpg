from entities.character import Character
from entities.rectangle import Rectangle


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