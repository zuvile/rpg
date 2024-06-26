from states.menu_state import MenuState
from actions import Actions

class InGameMenuState(MenuState):
    def __init__(self):
        options = ["SAVE", "LOAD", "EXIT"]
        option_handlers = {
            0: self.save_game,
            1: self.load_game,
            2: self.exit
        }
        super().__init__(options, option_handlers, Actions.IN_GAME_MENU)


    def save_game(self):
        #todo saving game
        return Actions.EXPLORE

    def load_game(self):
        pass
        return Actions.EXPLORE

    def exit(self):
        return Actions.EXIT