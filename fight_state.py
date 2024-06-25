from game_state import GameState
from pyray import *
from actions import *


class FightState(GameState):
    def __init__(self, player):
            self.player = player

    def draw(self, enemy):
        draw_texture(load_texture('assets/fight.png'), 0, 0, WHITE)
        self.player.draw()
        enemy.draw()

        draw_text("FIGHT", 640, 64, 20, RED)
        mouse_point = get_mouse_position()
        if check_collision_point_rec(mouse_point, Rectangle(640, 64, 128, 64)):
            draw_text("FIGHT", 640, 64, 20, GREEN)
            if is_mouse_button_down(MOUSE_LEFT_BUTTON):
                draw_text("ATTACKING ENEMY", 32, 32, 20, RED)
        if is_key_down(KEY_SPACE):
            return Actions.EXPLORE
        else:
            return Actions.FIGHT