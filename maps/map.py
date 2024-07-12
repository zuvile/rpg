from abc import ABC
from enum import Enum


class MapType(Enum):
    CASTLE_GROUNDS = 0
    CASTLE_INTERIOR = 1
    FIGHTING_AREA = 2


class Map(ABC):
    def add_walls(self):
        pass

    def add_friends(self):
        pass

    def add_enemies(self):
        pass

    def clear_dead(self):
        pass

    def update(self, characters):
        pass
