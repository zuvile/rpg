from pyray import *

class EnemyTurn:
    def __init__(self):
        self.done = False
        self.player = None
        self.enemy = None
        self.has_attacked = False

    def enter(self, game_state):
        self.player = game_state.player
        self.enemy = game_state.get_interactable()

    def draw(self):
        if self.has_attacked and not self.enemy.in_animation:
            self.done = True
            return

        if not self.has_attacked:
            self.enemy.do_attack()
            dmg = self.enemy.do_attack()
            self.player.apply_damage(dmg)
            self.has_attacked = True

        # self.message_stack.append("The enemy did " + str(dmg) + " damage to you!")

    def exit_state(self):
        self.has_attacked = False
        self.done = False
