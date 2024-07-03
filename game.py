from pyray import *
from modes.initial_menu_mode import InitialMenuMode
from actions import Actions
from save import Save


init_window(800, 480, "Game")
set_target_fps(60)
action = Actions.INITIAL_MENU
prev_action = None
initial_menu_mode = InitialMenuMode()
save = Save()
set_exit_key(KEY_NULL)
game_state = None

while not window_should_close():
    begin_drawing()

    if game_state is not None:
        game_state.render_stack.render()

    if action == Actions.INITIAL_MENU:
        action = initial_menu_mode.draw(None)
    if action == Actions.EXIT:
        end_drawing()
        break
    if action == Actions.CREATE_NEW_SAVE_FILE:
        game_state = save.create_new()
        game_state.render_stack.push(game_state.explore_mode)
        game_state.render_stack.push(game_state.story_mode)
        action = None
    if action == Actions.LOAD_SAVE_FILE:
        game_state = save.load()
    if action == Actions.SAVE_GAME:
        save.save(game_state)
    end_drawing()
close_window()
