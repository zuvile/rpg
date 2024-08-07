from util.cursor import Cursor
import pyray as rl
from util.sounds import play_sound
from entities.card import CardType
from modes.fight.card_gen import add_multi

class PlayerTurn(Cursor):
    def __init__(self):
        super().__init__()
        self.player = None
        self.enemy = None
        self.done = False
        self.card_played = False
        self.game_state = None

        self.action_handlers = {
            CardType.ATTACK: self.handle_attacking,
            CardType.HEAL: self.handle_healing,
            CardType.BUFF: self.handle_buffing,
            CardType.DEBUFF: self.handle_debuff,
            CardType.ADD_TO_OWN_PILE: self.add_to_own_pile,
            CardType.ADD_TO_ENEMY_PILE: self.add_to_enemy_pile
        }

    def enter(self, game_state):
        self.player = game_state.player
        self.enemy = game_state.get_interactable()
        self.game_state = game_state
        self.player.deck.update()

    def play_card(self):
        if rl.is_key_pressed(rl.KEY_ENTER):
            self.player.deck.play_card(self.cursor_index)

    def draw(self):
        if self.card_played and not self.player.in_animation() and not self.player.deck.in_animation():
            self.done = True
            return
        self.player.deck.draw_discard()
        self.player.deck.draw_pile()
        if not self.enemy.in_animation():
            self.player.deck.draw_card_deck(self.cursor_index)

        #wait for animations to finish
        if self.player.in_animation() or self.player.deck.in_animation():
            return
        self.player.deck.update()
        if self.player.deck.current_card is None:
            self.move_cursor_horizontal(len(self.player.deck.hand))
            self.play_card()
        else:
            self.action_handlers[self.player.deck.current_card.type]()
            self.card_played = True
            self.cursor_index = 0

    def handle_attacking(self):
        self.player.start_attack()
        play_sound("slash.wav")
        pts = self.player.deck.current_card.get_damage()
        self.enemy.apply_damage(pts)
        self.game_state.add_to_log("You did " + str(pts) + " DMG")

    def handle_healing(self):
        play_sound("heal.wav")
        self.player.add_health(self.player.deck.current_card.get_heal())
        self.game_state.add_to_log("You healed:" + str(self.player.deck.current_card.get_heal()) + " HP")

    def handle_buffing(self):
        play_sound("buff.wav")
        self.player.start_buffing()
        self.player.deck.buff_all_cards(self.player.deck.current_card)
        self.game_state.add_to_log("Buffed: " + str(self.player.deck.current_card.buff))

    def exit_state(self):
        self.card_played = False
        self.done = False
        self.player.end_attack()

    def handle_debuff(self):
        play_sound('debuff.wav')
        self.player.start_buffing()
        self.player.apply_damage(self.player.deck.current_card.get_heal())

    def add_to_enemy_pile(self):
        self.player.start_buffing()
        add_multi(self.player.deck.current_card.card, self.player.deck.current_card.multiplier, self.enemy)

    def add_to_own_pile(self):
        self.player.start_buffing()
        add_multi(self.player.deck.current_card.card, self.player.deck.current_card.multiplier, self.player)
