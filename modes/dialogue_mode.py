from entities.friendly import Friendly
from modes.game_mode import GameMode
from pyray import *
from actions import *
from dialogue import Dialogue
from cursor import Cursor
import textures

class DialogueMode(GameMode, Cursor):
    def __init__(self):
        super().__init__()
        self.dialogue = Dialogue()
        self.trees = self.dialogue.load_dialogue_trees()
        first_key = next(iter(self.trees))
        self.tree = self.trees[first_key]

        self.curr_page = 0
        self.done_reading = True

    def draw(self, game_state):
        map = game_state.map
        friend = map.friends[0]
        self.draw_scene(friend)
        idx = self.write_text(game_state)
        if self.done_reading:
            return self.advance_to_next_node(idx)

        return Actions.DIALOGUE

    def advance_to_next_node(self, idx):
        if self.tree.jmp is not None:
            self.tree = self.trees[self.tree.jmp]
            return Actions.DIALOGUE
        if len(self.tree.children) == 0:
            return Actions.EXPLORE

        self.tree = self.tree.children[idx]
        return Actions.DIALOGUE

    def write_choices(self):
        self.done_reading = False
        y = 13 * 32
        idx = 0
        for choices in self.tree.children:
            color = GREEN if idx == self.cursor_index else WHITE
            draw_text(choices.text, 2 * 32, y, 15, color)
            y += 32
            idx += 1

    def make_choice(self, game_state):
        if is_key_pressed(KEY_ENTER):
            rel_mods = self.tree.children[self.cursor_index].rel_mods
            #there's a better way to do this
            for key, value in rel_mods.items():
                for friend in game_state.map.friends:
                    if friend.name == key:
                        friend.rel += value
            self.done_reading = True
            return self.cursor_index

    # Write text and choices. Return 0 if no choice was made, otherwise return choice index
    def write_text(self, game_state):
        pages = [self.tree.text[i:i+64] for i in range(0, len(self.tree.text), 64)]
        if self.curr_page == len(pages) and len(self.tree.children) > 1:
            self.write_choices()
            self.move_cursor(len(self.tree.children))
            return self.make_choice(game_state)

        elif self.curr_page >= len(pages):
            self.curr_page = 0
            self.done_reading = True
            return 0
        else:
            self.done_reading = False
        draw_text(pages[self.curr_page], 2 * 32, 13 * 32, 15, WHITE)
        if is_key_pressed(KEY_ENTER):
            self.curr_page += 1
        return 0

    def draw_scene(self, friend):
        if self.tree.render is not None:
            texture = load_texture('assets/backgrounds/' + self.tree.render)
            draw_texture(texture, 0, 0, WHITE)
        draw_rectangle(0, 0, 200, 32, RAYWHITE)
        draw_text("Rel pts:" + str(friend.rel), 0, 0, 20, BLACK)
        draw_rectangle(0, 352, 800, 128, BLACK)
        sub_texture = Rectangle(0, 0, 64, 64)
        scale = 3

        origin = Vector2(0, 0)
        portrait_width = sub_texture.width * scale
        x = get_screen_width() - portrait_width
        destination = Rectangle(x, 300, sub_texture.width * scale, sub_texture.height * scale)
        textures.load_texture(friend.portrait)
        portrait_texture = textures.id_to_raylib(friend.portrait)
        draw_texture_pro(portrait_texture, sub_texture, destination, origin, 0, WHITE)

