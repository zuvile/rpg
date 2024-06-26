from states.menu_state import MenuState
from actions import Actions

class InitialMenuState(MenuState):
    def __init__(self):
        options = ["START", "LOAD", "EXIT"]
        option_handlers = {
            0: self.start_game,
            1: self.load_game,
            2: self.exit
        }
        super().__init__(options, option_handlers, Actions.INITIAL_MENU)

    def start_game(self):
        return Actions.EXPLORE

    def load_game(self):
        return Actions.EXPLORE

    def exit(self):
        return Actions.EXIT
