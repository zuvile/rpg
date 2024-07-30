from pyray import *
from modes.initial_menu_mode import InitialMenuMode
from actions import Actions
from util.save import Save

#640x360
init_window(1920, 1080, "Game")
init_audio_device()
set_target_fps(60)
action = Actions.INITIAL_MENU
prev_action = None
initial_menu_mode = InitialMenuMode()
save = Save()
set_exit_key(KEY_NULL)
game_state = None
render_texture = load_render_texture(640, 360)
while not window_should_close():
    begin_texture_mode(render_texture)
    clear_background(RAYWHITE)
    begin_drawing()

    if game_state is not None:
        game_state.update()
        game_state.render()

    if action == Actions.INITIAL_MENU:
        action = initial_menu_mode.draw(None)
    if action == Actions.EXIT:
        end_drawing()
        break
    if action == Actions.CREATE_NEW_SAVE_FILE:
        game_state = save.create_new()
        game_state.push_new_explore_mode()
        game_state.push_new_story_mode()
        action = None
    if action == Actions.LOAD_SAVE_FILE:
        game_state = save.load()
    if action == Actions.SAVE_GAME:
        save.save(game_state)
    end_texture_mode()
    source_rect = Rectangle(0, 0, render_texture.texture.width, -render_texture.texture.height)
    dest_rect = Rectangle(0, 0, render_texture.texture.width * 3, render_texture.texture.height * 3)
    origin = Vector2(0, 0)
    if game_state is not None:
        draw_texture_pro(render_texture.texture, source_rect, dest_rect, origin, 0, game_state.effects.get_color())
    else:
        draw_texture_pro(render_texture.texture, source_rect, dest_rect, origin, 0, WHITE)
    end_drawing()
close_window()
