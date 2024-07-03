from modes.game_mode import GameMode
from pyray import *
import textures
from cursor import Cursor


class TalkMode(GameMode, Cursor):
    def __init__(self, mode):
        super().__init__()
        self.curr_page = 0
        self.done_reading = True
        self.tree = None
        self.trees = []
        self.del_keys = []
        self.current_interactable = None
        self.mode = mode

    def set_dialogue_trees(self, trees):
        if not self.trees:
            self.trees = trees

    def draw(self, game_state):
        if not game_state.is_layer_top(self):
            return
        if len(self.trees) == 0:
            return self.write_nothing_say(game_state)
        if game_state.last_fight_won is not None and game_state.last_fight_won:
            self.tree = self.tree.children[0].children[0]
            game_state.last_fight_won = None
        elif game_state.last_fight_won is not None and not game_state.last_fight_won:
            self.tree = self.tree.children[1].children[0]
            game_state.last_fight_won = None

        if self.tree is None:
            first_key = next(iter(self.trees))
            self.del_keys.append(first_key)
            self.tree = self.trees[first_key]
        self.draw_scene()
        idx = self.write_text(game_state)
        if self.current_interactable is not None:
            self.draw_portrait()
        if self.done_reading:
            return self.advance_to_next_node(idx, game_state)

    def advance_to_next_node(self, idx, game_state):
        if self.tree.jmp is not None:
            self.del_keys.append(self.tree.jmp)
            self.tree = self.trees[self.tree.jmp]
            return
        if self.tree.init_fight:
            self.done_reading = False
            game_state.push_fight_mode()
            return

        if len(self.tree.children) == 0:
            self.remove_read_dialogue()
            game_state.pop_render_layer()
            return

        self.tree = self.tree.children[idx]

    def remove_read_dialogue(self):
        for key in self.del_keys:
            del self.trees[key]

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
            # there's a better way to do this
            for key, value in rel_mods.items():
                for friend in game_state.map.friends:
                    if friend.name == key:
                        friend.rel += value
            self.done_reading = True
            return self.cursor_index

    # Write text and choices. Return 0 if no choice was made, otherwise return choice index
    def write_text(self, game_state):
        self.set_interactable(game_state, self.tree)
        pages = [self.tree.text[i:i + 64] for i in range(0, len(self.tree.text), 64)]
        if self.curr_page == len(pages) and len(self.tree.children) > 1 and not self.tree.auto_choice:
            self.write_choices()
            self.move_cursor(len(self.tree.children))
            return self.make_choice(game_state)

        elif self.curr_page >= len(pages):
            self.curr_page = 0
            self.done_reading = True
            return 0
        else:
            self.done_reading = False
        if self.current_interactable is not None:
            draw_text(self.current_interactable.name.upper(), 2 * 32, 12 * 32, 15, SKYBLUE)
        else:
            draw_text("ME", 2 * 32, 12 * 32, 15, SKYBLUE)
        draw_text(pages[self.curr_page], 2 * 32, 13 * 32, 15, WHITE)
        if is_key_pressed(KEY_ENTER):
            self.curr_page += 1
        return 0

    def set_interactable(self, game_state, tree):
        speaker = tree.speaker
        for friend in game_state.map.friends:
            if friend.name.lower() == speaker.lower():
                self.current_interactable = friend
                return
        self.current_interactable = None
        return

    def draw_portrait(self):
        draw_rectangle(0, 0, 200, 32, RAYWHITE)
        draw_text("Rel pts:" + str(self.current_interactable.rel), 0, 0, 20, BLACK)
        origin = Vector2(0, 0)
        sub_texture = Rectangle(0, 0, 64, 64)
        scale = 3
        portrait_width = sub_texture.width * scale
        x = get_screen_width() - portrait_width
        destination = Rectangle(x, 300, sub_texture.width * scale, sub_texture.height * scale)
        textures.load_texture(self.current_interactable.portrait)
        portrait_texture = textures.id_to_raylib(self.current_interactable.portrait)
        draw_texture_pro(portrait_texture, sub_texture, destination, origin, 0, WHITE)

    def write_nothing_say(self, game_state):
        draw_rectangle(0, 352, 800, 128, BLACK)
        draw_text("There's nothing to talk about now", 2 * 32, 13 * 32, 15, WHITE)
        if is_key_pressed(KEY_ENTER):
            game_state.pop_render_layer()

    def draw_scene(self):
        if self.tree.render is not None:
            texture = load_texture('assets/backgrounds/' + self.tree.render)
            draw_texture(texture, 0, 0, WHITE)

        draw_rectangle(0, 352, 800, 128, BLACK)
