from friendly import Friendly
from states.game_state import GameState
from pyray import *
from actions import *
from dialogue import Dialogue

class DialogueState(GameState):
    def __init__(self):
        self.portrait_texture = load_texture('assets/portraits/cassius.png')
        self.dialogue = Dialogue()
        self.tree = self.dialogue.load_dialogue_tree()
        self.cursor_index = 0

    def draw(self, player, map):
        draw_rectangle(0, 0, 200, 32, RAYWHITE)
        friend = map.friends[0]
        draw_text("Rel pts:" + str(friend.rel), 0, 0, 20, BLACK)
        draw_rectangle(0, 352, 800, 128, BLACK)
        sub_texture = Rectangle(48, 0, 46, 64)
        scale = 2
        origin = Vector2(0, 0)
        portrait_width = sub_texture.width * scale
        x = get_screen_width() - portrait_width
        destination = Rectangle(x, 353, sub_texture.width * scale, sub_texture.height * scale)
        draw_texture_pro(self.portrait_texture, sub_texture, destination, origin, 0, WHITE)
        if len(self.tree.children) == 1:
            self.write_text()
        if len(self.tree.children) > 1:
            self.write_choices()
            self.move_cursor()
            self.make_choice(friend)
        if len(self.tree.children) == 0:
            self.write_text()
            if is_key_pressed(KEY_ENTER):
                return Actions.EXPLORE
        if is_key_pressed(KEY_ENTER):
            self.tree = self.tree.children[0]

        return Actions.DIALOGUE

    def write_choices(self):
        y = 12 * 32
        idx = 0
        for choices in self.tree.children:
            color = GREEN if idx == self.cursor_index else WHITE
            draw_text(choices.text, 2 * 32, y, 15, color)
            y += 32
            idx += 1

    def make_choice(self, friend: Friendly):
        if is_key_pressed(KEY_ENTER):
            friend.rel += self.tree.children[self.cursor_index].rel_mod
            print(self.tree.children[self.cursor_index].rel_mod)
            self.tree = self.tree.children[self.cursor_index]

    def write_text(self):
        text = self.tree.text
        if len(text) < 62:
            draw_text(self.tree.text, 2 * 32, 12 * 32, 15, WHITE)
        else:
            # todo don't split in the middle of the word
            draw_text(text[:32], 2 * 32, 12 * 32, 15, WHITE)
            draw_text(text[32:], 2 * 32, 13 * 32, 15, WHITE)

    def move_cursor(self):
        if is_key_pressed(KEY_W):
            self.cursor_index = (self.cursor_index - 1) % len(self.tree.children)
        if is_key_pressed(KEY_S):
            self.cursor_index = (self.cursor_index + 1) % len(self.tree.children)

