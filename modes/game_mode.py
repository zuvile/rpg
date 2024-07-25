from abc import ABC, abstractmethod


class GameMode(ABC):
    @abstractmethod
    def draw(self, game_state):
        pass

    def exit(self, game_state):
        game_state.camera.reset()

