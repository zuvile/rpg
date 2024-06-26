from states.game_state import GameState
from pyray import *


class MenuState(GameState):
    def __init__(self, options, option_handlers, action):
        self.options = options
        self.cursor_index = 0
        self.prev_key_w_state = False
        self.prev_key_s_state = False
        self.prev_key_enter_state = False
        self.option_handlers = option_handlers
        self.action = action

    def draw(self, player=None, map=None):
        self.draw_ui(self.options)
        key_w_state = is_key_down(KEY_W)
        key_s_state = is_key_down(KEY_S)
        key_enter_state = is_key_down(KEY_ENTER)
        self.move_cursor(self.cursor_index, len(self.options), key_w_state, key_s_state)
        if key_enter_state:
            return self.option_handlers[self.cursor_index]()
        self.prev_key_w_state = key_w_state
        self.prev_key_s_state = key_s_state
        self.prev_key_enter_state = key_enter_state

        return self.action

    def draw_ui(self, options):
        draw_rectangle(0, 0, 800, 600, BLACK)

        x = 640
        y = 65

        for index, option in enumerate(options):
            colour = RED
            if self.cursor_index == index:
                colour = GREEN
            draw_text(option, x, y, 20, colour)
            y += 32

    def move_cursor(self, curr, length, key_w_state, key_s_state):
        if ((key_w_state and not self.prev_key_w_state) or
                (key_s_state and not self.prev_key_s_state)):
            if (key_w_state):
                self.cursor_index = (curr - 1) % length
            if (key_s_state):
                self.cursor_index = (curr + 1) % length
