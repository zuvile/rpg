from pyray import *
from modes.explore_mode import ExploreMode
from modes.fight_mode import FightMode
from modes.dialogue_mode import DialogueMode
from modes.initial_menu_mode import InitialMenuMode
from modes.in_game_menu_mode import InGameMenuMode
from modes.story_mode import StoryMode
from actions import Actions
from save import Save

init_window(800, 480, "Game")
set_target_fps(60)
action = Actions.INITIAL_MENU
explore_mode = ExploreMode()
fight_mode = FightMode()
dialogue_mode = DialogueMode()
initial_menu_mode = InitialMenuMode()
in_game_menu_mode = InGameMenuMode()
story_mode = StoryMode()

save = Save()
set_exit_key(KEY_NULL)
game_state = None

while not window_should_close():
    begin_drawing()
    if action == Actions.EXIT:
        end_drawing()
        break
    if action == Actions.CREATE_NEW_SAVE_FILE:
        game_state = save.create_new()
        action = Actions.STORY
    if action == Actions.LOAD_SAVE_FILE:
        game_state = save.load()
        action = Actions.EXPLORE
    if action == Actions.SAVE_GAME:
        save.save(game_state)
        action = Actions.EXPLORE
    if action == Actions.INITIAL_MENU:
        action = initial_menu_mode.draw(None)


    if game_state is not None:
        if action == Actions.EXPLORE:
            game_state.map.update()
            action = explore_mode.draw(game_state)
        if action == Actions.FIGHT:
            action = fight_mode.draw(game_state)
        if action == Actions.STORY:
            action = story_mode.draw(game_state)
        if action == Actions.DIALOGUE:
            action = dialogue_mode.draw(game_state)
        if action == Actions.IN_GAME_MENU:
            action = in_game_menu_mode.draw(game_state)
    end_drawing()
close_window()

