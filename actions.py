from enum import Enum


class Actions(Enum):
    EXPLORE = 1
    FIGHT = 2
    DIALOGUE = 3
    INITIAL_MENU = 4
    IN_GAME_MENU = 5
    EXIT = 6
    CREATE_NEW_SAVE_FILE = 7
    LOAD_SAVE_FILE = 8
    SAVE_GAME = 9
    STORY = 10
