from modes.talk_mode import TalkMode
from dialogue import Dialogue
from actions import Actions

class StoryMode(TalkMode):
    def __init__(self):
        super().__init__(Actions.STORY)

    def draw(self, game_state):
        trees = self.get_trees_by_day(game_state.day)
        if trees is None:
            return Actions.EXPLORE

        super().set_dialogue_trees(trees)
        return super().draw(game_state)

    def get_trees_by_day(self, day):
        dialogue = Dialogue()
        if day == 1:
            return dialogue.load_dialogue_trees('dialogue_intro.txt')
