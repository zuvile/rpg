from game_state import GameState
from pyray import *
from actions import *


class FightState(GameState):
    def __init__(self, player):
            self.player = player
            self.cursor_index = 0
            self.prev_key_w_state = False
            self.prev_key_s_state = False
            self.prev_key_enter_state = False
            self.end_of_fight = False
            self.message = "You are in a fight!"

    def draw(self, enemy):
        draw_texture(load_texture('assets/fight.png'), 0, 0, WHITE)
        self.player.draw()
        enemy.draw()
        x = 640
        y = 65

        if self.end_of_fight:
            draw_text("You won! Press Enter to continue", 2 * 32, 10 * 32, 32, GREEN)
            if is_key_down(KEY_ENTER) and not self.prev_key_enter_state:
                self.end_of_fight = False
                return Actions.EXPLORE
        options = ["ATTACK", "SPELL", "RUN AWAY"]
        draw_text("Player HP: " + str(self.player.hp), 2 * 32, 12 * 32, 32, RED)
        draw_text("Enemy HP: " + str(enemy.hp), 2 * 32, 13 * 32, 32, RED)
        draw_text(self.message, 2 * 32, 14 * 32, 32, RED)

        key_w_state = is_key_down(KEY_W)
        key_s_state = is_key_down(KEY_S)
        key_enter_state = is_key_down(KEY_ENTER)

        if ((key_w_state and not self.prev_key_w_state) or
                (key_s_state and not self.prev_key_s_state)):
            self.cursor_index = self.move_cursor(self.cursor_index, len(options), "UP" if key_w_state else "DOWN")

        if key_enter_state and not self.prev_key_enter_state:
            if options[self.cursor_index] == "ATTACK":
                dmg = self.player.do_attack()
                self.message = "You attacked for " + str(dmg) + " damage"
                draw_text(self.message, 2 * 32, 14 * 32, 32, RED)
                enemy.apply_damage(dmg)
                if not enemy.is_alive():
                    self.end_of_fight = True

        self.prev_key_w_state = key_w_state
        self.prev_key_s_state = key_s_state
        self.prev_key_enter_state = key_enter_state

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
