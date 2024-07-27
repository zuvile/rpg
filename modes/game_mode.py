from abc import ABC, abstractmethod
from util.sounds import stop_sound

class GameMode(ABC):
    @abstractmethod
    def draw(self, game_state):
        pass

    def exit(self, game_state):
        game_state.camera.reset()
        stop_sound()
