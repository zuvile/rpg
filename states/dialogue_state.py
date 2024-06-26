from states.game_state import GameState
from pyray import *
from actions import *

class DialogueState(GameState):
    def draw(self, player, map):
        draw_rectangle(0, 352, 800, 128, BLACK)
        draw_rectangle(20 * 32, 10 * 32, 160, 260, BLUE)
        dialogue = map.friends[0].talk()
        draw_text(dialogue, 2 * 32, 12 * 32, 20, WHITE)
        if is_key_down(KEY_ENTER):
            return Actions.EXPLORE
        return Actions.DIALOGUE
