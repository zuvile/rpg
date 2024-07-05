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
        self.is_healing = False
        self.heal_animation_start_time = 0
        self.move_animation_start_time = 0
        self.is_walking = False

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

    def draw(self):
        draw_color = rl.WHITE
        if self.is_healing:
            draw_color = rl.GREEN
            if rl.get_time() - self.heal_animation_start_time > 1:
                self.is_healing = False
                draw_color = rl.WHITE

        if self.is_walking:
            draw_color = rl.BLUE
            if rl.get_time() - self.move_animation_start_time > 1:
                self.is_walking = False
                draw_color = rl.WHITE

        super().draw(draw_color)

    def heal(self, health):
        self.hp += health
        if self.hp > 100:
            self.hp = 100
            self.is_healing = True
            self.heal_animation_start_time = rl.get_time()

    def auto_move(self, dx, dy):
        self.is_walking = True
        self.rec.x += dx
        self.rec.y += dy
        self.move_animation_start_time = rl.get_time()

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

    def in_animation(self):
        return self.is_walking or self.is_healing
