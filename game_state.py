from entities.character import Character
from typing import Optional
from dialogue import Dialogue
from render_stack import RenderStack
from modes.dialogue_mode import DialogueMode
from modes.fight_mode import FightMode
from modes.story_mode import StoryMode
from modes.explore_mode import ExploreMode



class GameState:
    def __init__(self, map, player):
        self.map = map
        self.player = player
        self.interacting_with: Optional[Character] = None
        self.dialogue = Dialogue()
        self.day = 0
        self.render_stack = RenderStack(self)
        self.dialogue_mode = DialogueMode()
        self.fight_mode = FightMode()
        self.story_mode = StoryMode()
        self.explore_mode = ExploreMode()

    def set_interactable(self, character: Character):
        self.interacting_with = character

    def clear_interactable(self):
        self.interacting_with = None

    def get_interactable(self):
        return self.interacting_with

    def advance_day(self):
        self.day += 1
        for friend in self.map.friends:
            friend.update_dialogue_trees()

    def render(self):
        self.render_stack.render()

