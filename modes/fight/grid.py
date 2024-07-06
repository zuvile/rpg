from pyray import *
from util.cursor import Cursor
from entities.card import CardType


class Grid(Cursor):
    def __init__(self):
        super().__init__()
        self.map_arr = [[0 for _ in range(19)] for _ in range(11)]
        self.cursor_point = Vector2(0, 0)
        self.current_card = None
        self.player = None

    def draw_grid(self, player, enemy, current_card, game_state):
        if self.cursor_point.x == 0 and self.cursor_point.y == 0:
            self.cursor_point = Vector2(player.rec.x, player.rec.y)

        semi_transparent_red = Color(255, 0, 0, 128)
        player_tile_x = player.rec.x // 32
        player_tile_y = player.rec.y // 32
        for row_index in range(len(self.map_arr)):
            for tile_index in range(len(self.map_arr[row_index])):
                if player_tile_x - current_card.range <= tile_index <= player_tile_x + current_card.range and \
                        player_tile_y - current_card.range <= row_index <= player_tile_y + current_card.range:
                    self.map_arr[row_index][tile_index] = 1
                else:
                    self.map_arr[row_index][tile_index] = 0

        for row_index in range(len(self.map_arr)):
            for tile_index in range(len(self.map_arr[row_index])):
                if self.map_arr[row_index][tile_index] == 1:
                    draw_rectangle(tile_index * 32, row_index * 32, 32, 32, semi_transparent_red)

        semi_transparent_green = Color(0, 255, 0, 128)
        self.move_omnidirectional(self.cursor_point.x, self.cursor_point.y, self.map_arr)
        origin = Vector2(0, 0)
        cursor_rect = Rectangle(self.cursor_point.x, self.cursor_point.y, 32, 32)
        draw_rectangle_pro(cursor_rect, origin, 0, semi_transparent_green)
        if is_key_pressed(KEY_ENTER) and self.valid_move(enemy, game_state, current_card.type):
            return self.cursor_point
        else:
            return None

    def valid_move(self, enemy, game_state, action):
        result = None
        if action == CardType.ATTACK:
            result = self.map_arr[int(self.cursor_point.y) // 32][
                         int(self.cursor_point.x) // 32] == 1 and enemy.rec.x == int(
                self.cursor_point.x) and enemy.rec.y == int(
                self.cursor_point.y)
            if not result:
                game_state.add_to_log("Invalid attack")

        elif action == CardType.MOVE:
            result = self.map_arr[int(self.cursor_point.y) // 32][int(self.cursor_point.x) // 32] == 1
            if not result:
                game_state.add_to_log("Invalid move")

        return result
