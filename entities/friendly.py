from entities.character import Character
from dialogue.dialogue import Dialogue
import pyray as rl
from entities.character_elements import draw_health_bar

class Friendly(Character):
    def __init__(self, name, portrait, deck, texture, sub_texture, current_map, x=0, y=0, ac=5, hp=30):
        self.portrait = portrait
        self.name = name
        scale = 1
        self.dialogue_trees = []
        self.rel = 0
        self.ac = ac
        self.hp = hp
        self.is_attacking = False
        self.animation_start_time = 0
        self.move_speed = 1.0
        self.last_move_time = 0
        self.path_index = 0
        self.is_walking = False
        self.path = []
        self.move_animation_start_time = 0
        self.attack_animation_start_time = 0
        self.current_map = current_map

        super().__init__(texture, sub_texture, scale, deck, current_map, x, y, 32, ac, hp)

    def update_dialogue_trees(self, file_path):
        dialogue = Dialogue()
        trees = dialogue.load_dialogue_trees(file_path)
        self.dialogue_trees = trees

    def in_animation(self):
        return self.is_attacking

    def get_dialogue_trees(self):
        return self.dialogue_trees

    def do_attack(self):
        self.is_attacking = True
        self.animation_start_time = rl.get_time()

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
                next_pos_x, next_pos_y = self.path[self.path_index]
                self.rec.x = next_pos_x * 32
                self.rec.y = next_pos_y * 32
                self.path_index += 1
                self.last_move_time = rl.get_time()
            else:
                self.is_walking = False
        super().draw(draw_color)

    def auto_move(self, path):
        self.is_walking = True
        self.path_index = 0
        self.move_animation_start_time = rl.get_time()
        self.last_move_time = rl.get_time()
        self.path = path
