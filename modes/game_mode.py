from abc import ABC, abstractmethod


class GameMode(ABC):
    @abstractmethod
    def draw(self, game_state):
        pass
