from entities.character import Character
from typing import Optional
from dialogue import Dialogue


class GameState:
    def __init__(self, map, player):
        self.map = map
        self.player = player
        self.interacting_with: Optional[Character] = None
        self.dialogue = Dialogue()
        self.day = 0

    def set_interactable(self, character: Character):
        self.interacting_with = character

    def clear_interactable(self):
        self.interacting_with = None

    def get_interactable(self):
        return self.interacting_with

    def advance_day(self):
        self.day += 1
        for friend in self.map.friends:
            friend.update_dialogue_trees(self.dialogue.get_dialogue_for_character(friend.name))
