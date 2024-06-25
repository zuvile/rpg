from pyray import *
from player import Player
from explore_state import ExploreState
from fight_state import FightState
from actions import Actions

init_window(800, 480, "Game")
set_target_fps(60)
player = Player(3 * 32, 3 * 32)
action = Actions.EXPLORE
explore_state = ExploreState()
fight_state = FightState(player)

while not window_should_close():
    begin_drawing()
    if action == Actions.EXPLORE:
        action = explore_state.draw(player)
    if action == Actions.FIGHT:
        action = fight_state.draw(explore_state.map['enemies'][0])
    end_drawing()
close_window()
