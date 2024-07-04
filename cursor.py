from pyray import *

class Cursor:
    def __init__(self):
        self.cursor_index = 0
        self.cursor_point = Vector2(0, 0)

    def move_cursor_vertical(self, length):
        if is_key_pressed(KEY_W):
            self.cursor_index = (self.cursor_index - 1) % length
        if is_key_pressed(KEY_S):
            self.cursor_index = (self.cursor_index + 1) % length

    def move_cursor_horizontal(self, length):
        if is_key_pressed(KEY_A):
            self.cursor_index = (self.cursor_index - 1) % length
        if is_key_pressed(KEY_D):
            self.cursor_index = (self.cursor_index + 1) % length


    def move_omnidirectional(self, start_x, start_y, map_arr, step=1):
        #todo check with map_arr
        if is_key_pressed(KEY_S):
            self.cursor_point = Vector2(start_x, start_y + step * 32)
        if is_key_pressed(KEY_W):
            self.cursor_point = Vector2(start_x, start_y - step * 32)
        if is_key_pressed(KEY_A):
            self.cursor_point = Vector2(start_x - step * 32, start_y)
        if is_key_pressed(KEY_D):
            self.cursor_point = Vector2(start_x + step * 32, start_y)

