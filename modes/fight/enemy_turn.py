from entities.card import CardType
from modes.fight.ai_card_picker import pick_card
from modes.fight.grid import Grid
from pyray import *

class EnemyTurn:
    def __init__(self):
        self.done = False
        self.player = None
        self.enemy = None
        self.log = None
        self.game_state = None
        self.current_card = None
        self.grid = Grid()
        self.has_moved = False
        self.card_played = False
        self.card_in_animation = False
        self.card_animation_start_time = 0

        self.action_handlers = {
            CardType.ATTACK: self.handle_attacking,
            CardType.HEAL: self.handle_healing,
            CardType.BUFF: self.handle_buffing,
        }

    def enter(self, game_state):
        self.player = game_state.player
        self.enemy = game_state.get_interactable()
        self.game_state = game_state

    def draw(self):
        if self.card_played and not self.enemy.in_animation() and not self.card_in_animation:
            self.done = True
            return

        #wait for animations to finish
        if self.enemy.in_animation():
            return

        if self.card_in_animation:
            self.draw_enemy_card(self.current_card)
            return

        if self.current_card is None:
            self.current_card = pick_card(self.enemy.deck, self.enemy.rec, self.player.rec)
            self.card_in_animation = True
            self.game_state.play_sound("play_card.wav")
            self.card_animation_start_time = get_time()
        elif not self.card_in_animation:
            self.action_handlers[self.current_card.type]()

    def exit_state(self):
        self.card_played = False
        self.has_moved = False
        self.done = False

    def handle_attacking(self):
        self.enemy.do_attack()
        self.game_state.play_sound("claw.wav")
        pts = self.current_card.get_damage()
        self.player.apply_damage(pts)
        self.game_state.add_to_log("Enemy did " + str(pts) + " DMG")
        self.current_card = None
        self.card_played = True
        self.game_state.camera.shake()


    def handle_healing(self):
        self.enemy.heal(self.current_card.get_heal())
        self.game_state.add_to_log("Enemy healed:" + str(self.current_card.get_heal()) + " HP")
        self.current_card = None
        self.card_played = True

    def handle_buffing(self):
        self.enemy.deck.buff_all_cards(self.current_card)
        self.card_played = True
        self.game_state.add_to_log("Enemy Buffed: " + str(self.current_card.buff))
        self.current_card = None
        self.card_played = True


    def draw_enemy_card(self, card):
        draw_rectangle(480, 64, 128, 160, WHITE)
        draw_text(card.name, 480, 64, 20, BLACK)
        draw_text(card.get_description(), 480, 96, 12, BLACK)

        if get_time() - self.card_animation_start_time > 1:
            self.card_in_animation = False
            self.card_animation_start_time = 0

