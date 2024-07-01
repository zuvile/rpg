from actions import Actions
from map import Map
from game_state import GameState
from entities.player import Player
import pickle


class Save:
    def __init__(self):
        self.save_game_file = 'game_state.pkl'

    def getGameState(self, action):
        if action == Actions.CREATE_NEW_SAVE_FILE:
            return self.create_new()
        if action == Actions.LOAD_SAVE_FILE:
            return self.load()

    def create_new(self):
        map = Map()
        player = Player(3 * 32, 3 * 32)
        game_state = GameState(map, player)
        game_state.advance_day()

        return game_state


    def save(self, game_state):
        with open(self.save_game_file, 'wb') as file:
            pickle.dump(game_state, file)

    def load(self):
        with open(self.save_game_file, 'rb') as file:
            game_state = pickle.load(file)
        return game_state


def identify_unpicklable_attribute(obj):
    for attr_name, attr_value in obj.__dict__.items():
        try:
            pickle.dumps(attr_value)
        except Exception as e:
            print(f"Cannot pickle the attribute '{attr_name}' of the object. Error: {str(e)}")



