from characters.create_characters import create_characters
from maps.castle_grounds import CastleGrounds
from maps.map import MapType
from game_state import GameState
from entities.player import Player
from util.camera import Camera


def create_new_game():
    maps = {}
    maps[MapType.CASTLE_GROUNDS] = CastleGrounds()

    player = Player(3 * 32, 3 * 32)
    player.set_map(MapType.CASTLE_GROUNDS)

    characters = create_characters()
    game_state = GameState(player, maps, characters)
    game_state.advance_day()
    game_state.camera = Camera()

    return game_state
