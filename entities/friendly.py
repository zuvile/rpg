from entities.character import Character
from dialogue.dialogue import Dialogue


class Friendly(Character):
    def __init__(self, name, portrait, deck, texture, sub_texture, current_map, hp, x, y):
        self.portrait = portrait
        self.name = name
        scale = 1
        self.dialogue_trees = []
        self.rel = 0
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

        super().__init__(texture, sub_texture, scale, deck, current_map, hp, x, y)

    def update_dialogue_trees(self, file_path):
        dialogue = Dialogue()
        trees = dialogue.load_dialogue_trees(file_path)
        self.dialogue_trees = trees

    def get_dialogue_trees(self):
        return self.dialogue_trees
