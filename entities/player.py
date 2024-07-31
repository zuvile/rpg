from entities.character import Character
from entities.rectangle import Rectangle
from entities.player_deck import PlayerDeck
from util.collision import should_init_fight, should_init_dialogue
import pyray as rl
from util.sounds import play_sound


class Player(Character):
    def __init__(self, x=0, y=0):
        texture = 'assets/rogues.png'
        sub_texture = Rectangle(64, 64, 32, 32)
        scale = 1
        self.attack = 10
        self.ac = 5
        self.hp = 100
        self.max_hp = 100
        self.magic = 1
        self.mana = 10
        self.dead = False
        super().__init__(texture, sub_texture, scale, x, y, self.hp, 32)
        self.deck = PlayerDeck()


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
            play_sound("footstep.mp3")
            self.rec.x += dx
            self.rec.y += dy
        if should_init_fight(self, game_state):
            game_state.push_fight_mode()
        if should_init_dialogue(self, game_state):
            game_state.push_new_dialogue_mode()

    def increase_magic_skill(self, modifier):
        self.magic += modifier

    def move_towards_enemy(self):
        self.rec.x = self.rec.x + 96

    def move_away_from_enemy(self):
        self.rec.x = self.rec.x - 96

    def set_deck(self, cards):
        self.deck = PlayerDeck(cards)

    def __repr__(self):
        return f"Player({self.rec.x}, {self.rec.y})"
