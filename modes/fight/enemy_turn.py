from entities.card import CardType
from modes.fight.ai_card_picker import pick_card
from modes.fight.grid import Grid
import pyray as rl
from util.sounds import play_sound

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
            CardType.ADD_TO_ENEMY_PILE: self.add_to_player_pile
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
            play_sound("play_card.wav")
            self.card_animation_start_time = rl.get_time()
        elif not self.card_in_animation:
            self.action_handlers[self.current_card.type]()
            self.current_card = None
            self.card_played = True

    def exit_state(self):
        self.card_played = False
        self.has_moved = False
        self.done = False

    def handle_attacking(self):
        self.enemy.do_attack()
        play_sound("claw.wav")
        pts = self.current_card.get_damage()
        self.player.apply_damage(pts)
        self.game_state.add_to_log("Enemy did " + str(pts) + " DMG")
        self.game_state.shake_cam()

    def add_to_player_pile(self):
        cards = [self.current_card.card for _ in range(3)]
        self.player.deck.add_to_pile(cards)

    def handle_healing(self):
        self.enemy.heal(self.current_card.get_heal())
        self.game_state.add_to_log("Enemy healed:" + str(self.current_card.get_heal()) + " HP")

    def handle_buffing(self):
        self.enemy.deck.buff_all_cards(self.current_card)
        self.card_played = True
        self.game_state.add_to_log("Enemy Buffed: " + str(self.current_card.buff))


    def draw_enemy_card(self, card):
        rl.draw_rectangle(480, 64, 128, 160, rl.WHITE)
        rl.draw_text(card.name, 480, 64, 20, rl.BLACK)
        # rl.draw_text(card.get_description(), 480, 96, 12, rl.BLACK)

        if rl.get_time() - self.card_animation_start_time > 1:
            self.card_in_animation = False
            self.card_animation_start_time = 0

