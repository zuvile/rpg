from pyray import *
from util.cursor import Cursor
from entities.card import CardType
from util.path_finding import find_path as fp, get_neighbours, get_distance


class Grid(Cursor):
    def __init__(self):
        super().__init__()
        self.map_arr = [[0 for _ in range(19)] for _ in range(11)]
        self.cursor_point = Vector2(0, 0)
        self.current_card = None
        self.player = None

    def select_square(self, player, enemy, current_card, game_state):
        if self.cursor_point.x == 0 and self.cursor_point.y == 0:
            self.cursor_point = Vector2(player.rec.x, player.rec.y)

        if current_card.type == CardType.DASH_AND_SLASH:
            self.fill_grid_for_dash_and_slash(enemy, current_card)
        else:
            self.fill_grid_for_basic_range(player, current_card)

        semi_transparent_red = Color(255, 0, 0, 128)

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

    def fill_grid_for_basic_range(self, player, current_card):
        player_tile_x = player.rec.x // 32
        player_tile_y = player.rec.y // 32
        for row_index in range(len(self.map_arr)):
            for tile_index in range(len(self.map_arr[row_index])):
                if player_tile_x - current_card.get_range() <= tile_index <= player_tile_x + current_card.get_range() and \
                        player_tile_y - current_card.get_range() <= row_index <= player_tile_y + current_card.get_range():
                    self.map_arr[row_index][tile_index] = 1
                else:
                    self.map_arr[row_index][tile_index] = 0

    def fill_grid_for_dash_and_slash(self, enemy, current_card):
        x = enemy.rec.x // 32
        y = enemy.rec.y // 32

        if current_card.type == CardType.DASH_AND_SLASH:
            possible_destinations = self.get_surounding_area(x, y)
            for row_index in range(len(self.map_arr)):
                for tile_index in range(len(self.map_arr[row_index])):
                    if [tile_index, row_index] in possible_destinations:
                        self.map_arr[row_index][tile_index] = 1
                    else:
                        self.map_arr[row_index][tile_index] = 0

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
        elif action == CardType.DASH_AND_SLASH:
            # maybe I should use card range here?
            result = self.map_arr[int(self.cursor_point.y) // 32][int(self.cursor_point.x) // 32] == 1
            if not result:
                game_state.add_to_log("Invalid dash and slash")

        return result

    def find_path(self, player, cursor_point):
        path = fp(player.rec, cursor_point, self.map_arr)

        return path

    def find_closest_to_player(self, player, enemy):
        player_point = tuple([player.rec.x // 32, player.rec.y // 32])
        enemy_point = tuple([enemy.rec.x // 32, enemy.rec.y // 32])
        neighbours = get_neighbours(player_point, self.map_arr)
        closest = None
        min_distance = 100000
        for neighbour in neighbours:
            distance = get_distance(neighbour, enemy_point)
            if distance < min_distance:
                min_distance = distance
                closest = neighbour
        if closest is not None:
            return Vector2(closest[0] * 32, closest[1] * 32)
        else:
            return None

    #todo the player is too far away, move to nearest square
    def find_closest_by_range(self, player, enemy):
        pass

    def get_surounding_area(self, x, y, range=1):
        return [[x, y - range],
                [x + range, y - range],
                [x + range, y],
                [x + range, y + range],
                [x, y + range],
                [x - range, y + range],
                [x - range, y],
                [x - range, y - range]]
