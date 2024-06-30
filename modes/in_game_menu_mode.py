from modes.menu_mode import MenuMode
from actions import Actions

class InGameMenuMode(MenuMode):
    def __init__(self):
        self.game_state = None
        options = ["SAVE", "LOAD", "EXIT"]
        option_handlers = {
            0: self.save_game,
            1: self.load_game,
            2: self.exit
        }
        super().__init__(options, option_handlers, Actions.IN_GAME_MENU)


    def save_game(self):
        return Actions.SAVE_GAME

    def load_game(self):
        pass
        return Actions.LOAD_SAVE_FILE

    def exit(self):
        return Actions.EXIT