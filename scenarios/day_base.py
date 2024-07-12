from abc import ABC, abstractmethod


class DayBase(ABC):
    @abstractmethod
    def load_day(self, game_state):
        self.load_entities(game_state)
        self.load_dialogues(game_state)

    @abstractmethod
    def load_dialogues(self, game_state):
        pass

    @abstractmethod
    def load_entities(self, game_state):
        pass
