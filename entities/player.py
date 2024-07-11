from entities.character import Character
from entities.rectangle import Rectangle
from entities.player_deck import PlayerDeck
from util.collision import should_init_fight, should_init_dialogue
import pyray as rl
import random
from entities.character_elements import draw_health_bar
from entities.character import CharacterType

class Player(Character):
    def __init__(self, x=0, y=0):
        texture = 'assets/rogues.png'
        sub_texture = Rectangle(64, 64, 32, 32)
        scale = 1
        self.attack = 10
        self.ac = 5
        self.hp = 100
        self.magic = 1
        self.mana = 10
        self.dead = False
        self.deck = PlayerDeck()
        self.is_healing = False
        self.is_attacking = False
        self.heal_animation_start_time = 0
        self.move_animation_start_time = 0
        self.attack_animation_start_time = 0
        self.move_speed = 1.0
        self.last_move_time = 0
        self.path_index = 0
        self.is_walking = False
        self.path = []
        self.type = CharacterType.PLAYER

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

    def draw(self, color=rl.WHITE):
        if self.is_in_fight:
            draw_health_bar(rl.GREEN, self)
        draw_color = rl.WHITE
        if self.is_healing:
            draw_color = rl.GREEN
            if rl.get_time() - self.heal_animation_start_time > 1:
                self.is_healing = False
                draw_color = rl.WHITE
        if self.is_walking and rl.get_time() - self.last_move_time >= self.move_speed:
            if self.path_index < len(self.path):
                next_pos = self.path[self.path_index]
                self.rec.x = next_pos[0] * 32  # Assuming each square is 32x32 pixels
                self.rec.y = next_pos[1] * 32
                self.path_index += 1
                self.last_move_time = rl.get_time()
            else:
                self.is_walking = False  # Finished walking
        if self.is_attacking:
            draw_color = rl.RED
            if rl.get_time() - self.attack_animation_start_time > 1:
                self.is_attacking = False
                draw_color = rl.WHITE

        super().draw(draw_color)

    def heal(self, health):
        self.hp += health
        if self.hp > 100:
            self.hp = 100
            self.is_healing = True
            self.heal_animation_start_time = rl.get_time()

    def auto_move(self, path):
        self.is_walking = True
        self.path_index = 0
        self.move_animation_start_time = rl.get_time()
        self.last_move_time = rl.get_time()
        self.path = path


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
        return self.is_walking or self.is_healing or self.is_attacking

    def do_attack(self):
        self.is_attacking = True
        self.attack_animation_start_time = rl.get_time()
