from modes.menu_mode import MenuMode
from actions import Actions
from save import Save
from modes.story_mode import StoryMode

class InitialMenuMode(MenuMode):
    def __init__(self):
        options = ["START", "LOAD", "EXIT"]
        option_handlers = {
            0: self.start_game,
            1: self.load_game,
            2: self.exit
        }
        super().__init__(options, option_handlers, Actions.INITIAL_MENU)

    def start_game(self):
        return Actions.CREATE_NEW_SAVE_FILE

    def load_game(self):
        return Actions.LOAD_SAVE_FILE

    def exit(self):
        return Actions.EXIT
