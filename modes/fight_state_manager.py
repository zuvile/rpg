from modes.fight.play_card import PlayCard
from modes.fight.enemy_turn import EnemyTurn

class FightStateManager:
    def __init__(self):
        self.states = {
            'card_select': PlayCard(),
            'enemy_turn': EnemyTurn()
        }
        self.current_state = None

    def set_state(self, state, game_state):
        #todo refactor
        if self.current_state is not None and self.states[state] == self.current_state:
            self.current_state.enter(game_state)
            return

        if state not in self.states:
            return

        if self.current_state is not None:
            self.current_state.exit_state()
        state = self.states[state]
        self.current_state = state
        self.current_state.enter(game_state)

    def update(self):
        if self.current_state is not None:
            self.current_state.update()

    def draw(self):
        if self.current_state is not None:
            self.current_state.draw()

    def current_state_done(self):
        return self.current_state.done
