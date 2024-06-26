from pyray import *
from player import Player
from states.explore_state import ExploreState
from states.fight_state import FightState
from states.dialogue_state import DialogueState
from states.initial_menu_state import InitialMenuState
from states.in_game_menu_state import InGameMenuState
from actions import Actions
from map import Map

init_window(800, 480, "Game")
set_target_fps(60)
player = Player(3 * 32, 3 * 32)
action = Actions.INITIAL_MENU
explore_state = ExploreState()
fight_state = FightState()
dialogue_state = DialogueState()
initial_menu_state = InitialMenuState()
in_game_menu_state = InGameMenuState()
map = Map()
set_exit_key(KEY_NULL)

while not window_should_close():
    begin_drawing()
    if action == Actions.EXIT:
        end_drawing()
        break
    if action == Actions.INITIAL_MENU:
        action = initial_menu_state.draw()
    if action == Actions.IN_GAME_MENU:
        action = in_game_menu_state.draw()
    if action == Actions.EXPLORE:
        action = explore_state.draw(player, map)
    if action == Actions.FIGHT:
        action = fight_state.draw(player, map)
    if action == Actions.DIALOGUE:
        action = dialogue_state.draw(player, map)
    end_drawing()
close_window()
