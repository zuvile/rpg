from entities.character import Character
from entities.rectangle import Rectangle
from dialogue.dialogue import Dialogue
import random
import pyray as rl
from entities.character_elements import draw_health_bar

class Friendly(Character):
    def __init__(self, name, portrait, x=0, y=0, attack=10, ac=5, hp=30, magic=1, mana=10):
        texture = 'assets/rogues.png'
        sub_texture = Rectangle(32, 128, 32, 32)
        self.portrait = portrait
        self.name = name
        scale = 1
        self.dialogue_trees = []
        self.rel = 0
        self.attack = attack
        self.ac = ac
        self.hp = hp
        self.magic = magic
        self.mana = mana
        self.is_attacking = False
        self.animation_start_time = 0

        super().__init__(texture, sub_texture, scale, x, y, attack, ac, hp, magic, mana)

    def update_dialogue_trees(self):
        dialogue = Dialogue()
        trees = dialogue.load_dialogue_trees('dialogue_files/cassius_dialogues.txt')
        self.dialogue_trees = trees

    def in_animation(self):
        return self.is_attacking

    def get_dialogue_trees(self):
        return self.dialogue_trees

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