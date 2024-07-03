from modes.game_mode import GameMode
from pyray import *
from cursor import Cursor


class MenuMode(GameMode, Cursor):
    def __init__(self, options, option_handlers, action):
        super().__init__()
        self.options = options
        self.option_handlers = option_handlers
        self.action = action

    def draw(self, game_state):
        self.draw_ui(self.options)

        self.move_cursor_vertical(len(self.options))
        if is_key_pressed(KEY_ENTER):
            return self.option_handlers[self.cursor_index]()

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
