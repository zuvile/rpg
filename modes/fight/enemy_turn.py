from physics import vector

class EnemyTurn:
    def __init__(self):
        self.done = False
        self.player = None
        self.enemy = None
        self.has_attacked = False
        self.log = None
        self.game_state = None

    def enter(self, game_state):
        self.player = game_state.player
        self.enemy = game_state.get_interactable()
        self.game_state = game_state

    def draw(self):
        if self.has_attacked and not self.enemy.in_animation():
            self.done = True
            return

        if not self.has_attacked:
            #todo something here maybe move?
            self.enemy.do_attack()
            dmg = self.enemy.do_attack()
            self.game_state.add_to_log("Enemy did " + str(dmg) + " DMG")
            self.player.apply_damage(dmg)
            self.has_attacked = True

    def exit_state(self):
        self.has_attacked = False
        self.done = False
