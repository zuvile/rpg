from actions import Actions
from game_state import GameState
from entities.player import Player
import pickle
from util import new_game_initializer


class Save:
    def __init__(self):
        self.save_game_file = '../game_state.pkl'

    def getGameState(self, action):
        if action == Actions.CREATE_NEW_SAVE_FILE:
            return self.create_new()
        if action == Actions.LOAD_SAVE_FILE:
            return self.load()

    def create_new(self):
        game_state = new_game_initializer.create_new_game()

        return game_state

    def save(self, game_state):
        with open(self.save_game_file, 'wb') as file:
            pickle.dump(game_state, file)

    def load(self):
        with open(self.save_game_file, 'rb') as file:
            game_state = pickle.load(file)
        return game_state



