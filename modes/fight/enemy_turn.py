from entities.card import CardType
from modes.fight.ai_card_picker import pick_card
from modes.fight.grid import Grid


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

        self.action_handlers = {
            CardType.ATTACK: self.handle_attacking,
            CardType.HEAL: self.handle_healing,
            CardType.MOVE: self.handle_moving,
            CardType.BUFF: self.handle_buffing,
            CardType.DASH_AND_SLASH: self.handle_dash_and_slash,
        }

    def enter(self, game_state):
        self.player = game_state.player
        self.enemy = game_state.get_interactable()
        self.game_state = game_state

    def draw(self):
        if self.card_played and not self.enemy.in_animation():
            self.done = True
            return

        #wait for animations to finish
        if self.enemy.in_animation():
            return
        if self.current_card is None:
            self.current_card = pick_card(self.enemy.deck, self.enemy.rec, self.player.rec)
        else:
            self.action_handlers[self.current_card.type]()

    def exit_state(self):
        self.card_played = False
        self.has_moved = False
        self.done = False

    def handle_attacking(self):
        self.enemy.do_attack()
        pts = self.current_card.get_damage()
        self.player.apply_damage(pts)
        self.game_state.add_to_log("Enemy did " + str(pts) + " DMG")
        self.current_card = None
        self.card_played = True

    def handle_healing(self):
        self.enemy.heal(self.current_card.get_heal())
        self.game_state.add_to_log("Enemy healed:" + str(self.current_card.get_heal()) + " HP")
        self.current_card = None
        self.card_played = True

    def handle_dash_and_slash(self):
        if self.has_moved:
            self.enemy.do_attack()
            pts = self.current_card.get_damage()
            self.player.apply_damage(pts)
            self.game_state.add_to_log("Enemy did " + str(pts) + " DMG")
            self.current_card = None
            self.has_moved = False
            self.card_played = True
        else:
            #get nearest square to player
            closest = self.grid.find_closest_to_player(self.player, self.enemy)
            path = self.grid.find_path(self.enemy, closest)
            self.enemy.auto_move(path)
            self.has_moved = True

    def handle_moving(self):
        closest = self.grid.find_closest_to_player(self.player, self.enemy)
        path = self.grid.find_path(self.enemy, closest)
        self.enemy.auto_move(path)
        self.has_moved = True
        self.card_played = True

    def handle_buffing(self):
        self.player.deck.buff_all_cards(self.current_card)
        self.card_played = True
        self.game_state.add_to_log("Buffed: " + str(self.current_card.buff))
        self.current_card = None
        self.card_played = True

