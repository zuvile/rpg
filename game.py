from pyray import *
from player import Player
from explore_state import ExploreState
from fight_state import FightState
from dialogue_state import DialogueState
from menu_state import MenuState
from actions import Actions
from map import Map

init_window(800, 480, "Game")
set_target_fps(60)
player = Player(3 * 32, 3 * 32)
action = Actions.MENU
explore_state = ExploreState()
fight_state = FightState()
dialogue_state = DialogueState()
menu_state = MenuState()
map = Map()


while not window_should_close():
    begin_drawing()
    if action == Actions.MENU:
        action = menu_state.draw()
    if action == Actions.EXPLORE:
        action = explore_state.draw(player, map)
    if action == Actions.FIGHT:
        # todo separate map to its own class
        action = fight_state.draw(player, map)
    if action == Actions.DIALOGUE:
        action = dialogue_state.draw(player, map)
    end_drawing()
close_window()
