from entities.character import Character
from typing import Optional

class GameState:
    def __init__(self, map, player):
        self.map = map
        self.player = player
        self.interacting_with: Optional[Character] = None

    def set_interactable(self, character: Character):
        self.interacting_with = character

    def clear_interactable(self):
        self.interacting_with = None

    def get_interactable(self):
        return self.interacting_with