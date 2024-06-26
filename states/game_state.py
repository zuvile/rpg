from abc import ABC, abstractmethod


class GameState(ABC):
    @abstractmethod
    def draw(self, player, map):
        pass
