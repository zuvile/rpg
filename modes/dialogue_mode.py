from cursor import Cursor
from modes.talk_mode import TalkMode

class DialogueMode(TalkMode, Cursor):
    def __init__(self):
        super().__init__()

    def draw(self, game_state):
        friend = game_state.get_interactable()
        trees = friend.get_dialogue_trees()

        super().set_dialogue_trees(trees)
        return super().draw(game_state)
