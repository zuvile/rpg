from entities.character import Character
from entities.rectangle import Rectangle
from dialogue import Dialogue

class Friendly(Character):
    def __init__(self, name, portrait, x=0, y=0, attack=10, ac=5, hp=30, magic=1, mana=10, dead=False):
        texture = 'assets/dorian.png'
        sub_texture = Rectangle(0, 0, 32, 32)
        self.portrait = portrait
        self.name = name
        scale = 2
        self.dialogue_trees = []
        self.rel = 0

        super().__init__(texture, sub_texture, scale, x, y)

    def update_dialogue_trees(self):
        dialogue = Dialogue()
        trees = dialogue.load_dialogue_trees('cassius_dialogues.txt')
        self.dialogue_trees = trees

    def get_dialogue_trees(self):
        return self.dialogue_trees

