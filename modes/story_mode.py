from modes.talk_mode import TalkMode
from dialogue.dialogue import Dialogue
from actions import Actions
from pyray import *

class StoryMode(TalkMode):
    def __init__(self):
        super().__init__(Actions.STORY)

    def draw(self, game_state):
        if not game_state.is_layer_top(self):
            return
        trees = self.get_dialogue_trees_by_day(game_state.day)
        if trees is None:
            game_state.pop_render_layer()
            return

        super().set_dialogue_trees(trees)
        super().draw(game_state)

    def get_dialogue_trees_by_day(self, day):
        dialogue = Dialogue()
        # todo cache
        if day == 0:
            return dialogue.load_dialogue_trees('dialogue_files/dialogue_intro.txt')
