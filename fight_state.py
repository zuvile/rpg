from game_state import GameState
from pyray import *
from actions import *


class FightState(GameState):
    def __init__(self, player):
            self.player = player
            self.cursor_index = 0
            self.prev_key_w_state = False
            self.prev_key_s_state = False

    def draw(self, enemy):
        draw_texture(load_texture('assets/fight.png'), 0, 0, WHITE)
        self.player.draw()
        enemy.draw()
        x = 640
        y = 65

        options = ["ATTACK", "SPELL", "RUN AWAY"]

        key_w_state = is_key_down(KEY_W)
        key_s_state = is_key_down(KEY_S)

        if ((key_w_state and not self.prev_key_w_state) or
                (key_s_state and not self.prev_key_s_state)):
            self.cursor_index = self.move_cursor(self.cursor_index, len(options), "UP" if key_w_state else "DOWN")

        self.prev_key_w_state = key_w_state
        self.prev_key_s_state = key_s_state

        for index, option in enumerate(options):
            colour = RED
            if self.cursor_index == index:
                colour = GREEN
            draw_text(option, x, y, 20, colour)
            y += 32

        return Actions.FIGHT


    def move_cursor(self, curr, length, direction):
        if (direction == "UP"):
            return (curr - 1) % length
        if (direction == "DOWN"):
            return (curr + 1) % length
        return curr
