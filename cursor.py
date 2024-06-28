from pyray import *

class Cursor:
    def __init__(self):
        self.cursor_index = 0

    def move_cursor(self, length):
        if is_key_pressed(KEY_W):
            self.cursor_index = (self.cursor_index - 1) % length
        if is_key_pressed(KEY_S):
            self.cursor_index = (self.cursor_index + 1) % length
