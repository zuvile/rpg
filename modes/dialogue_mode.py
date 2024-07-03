from cursor import Cursor
from modes.talk_mode import TalkMode
from actions import Actions

class DialogueMode(TalkMode, Cursor):
    def __init__(self):
        super().__init__(Actions.DIALOGUE)

    def draw(self, game_state):
        friend = game_state.get_interactable()
        trees = friend.get_dialogue_trees()

        super().set_dialogue_trees(trees)
        super().draw(game_state)
