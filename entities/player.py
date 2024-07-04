from entities.character import Character
from entities.rectangle import Rectangle
from entities.deck import Deck
from collision import should_init_fight, should_init_dialogue
import pyray as rl

class Player(Character):
    def __init__(self, x=0, y=0):
        texture = 'assets/player.png'
        sub_texture = Rectangle(0, 0, 32, 32)
        scale = 2
        self.attack = 10
        self.ac = 5
        self.hp = 100
        self.magic = 1
        self.mana = 10
        self.dead = False
        self.deck = Deck()

        super().__init__(texture, sub_texture, scale, x, y, 62, self.attack, self.ac, self.hp, self.magic, self.mana)

    def move(self, game_state):
        if rl.is_key_down(rl.KEY_W):
            return self.move_player(0, -2, game_state)
        if rl.is_key_down(rl.KEY_S):
            return self.move_player(0, 2, game_state)
        if rl.is_key_down(rl.KEY_A):
            return self.move_player(-2, 0, game_state)
        if rl.is_key_down(rl.KEY_D):
            return self.move_player(2, 0, game_state)

    def move_player(self, dx, dy, game_state):
        if self.can_move(dx, dy, game_state):
            self.rec.x += dx
            self.rec.y += dy
        if should_init_fight(self, game_state):
            game_state.push_fight_mode()
        if should_init_dialogue(self, game_state):
            game_state.push_new_dialogue_mode()

    def increase_magic_skill(self, modifier):
        self.magic += modifier

