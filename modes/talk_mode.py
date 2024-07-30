from modes.game_mode import GameMode
from pyray import *
from util import textures
from util.cursor import Cursor
from util.textures import load_texture
from config import SCREEN_WIDTH, SCREEN_HEIGHT


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
        self.showing_heart = False
        self.heart_animation_start_time = 0
        self.liked_choice = False
        self.background = None
        self.name_pos = (SCREEN_WIDTH // 10, SCREEN_HEIGHT - 96)
        self.text_pos = (SCREEN_WIDTH // 10, SCREEN_HEIGHT - 96 + 32)
        self.font_size = 8
        self.portrait_pos = (SCREEN_WIDTH - 128, SCREEN_HEIGHT - 128)

    def set_dialogue_trees(self, trees):
        if not self.trees:
            self.trees = trees

    def draw(self, game_state):
        if not game_state.is_layer_top(self):
            return

        if len(self.trees) == 0:
            return self.write_nothing_say(game_state)

        if game_state.fight_from_dialogue:
            self.advance_after_fight(game_state)

        if self.tree is None:
            first_key = next(iter(self.trees))
            self.del_keys.append(first_key)
            self.tree = self.trees[first_key]
        self.draw_scene(game_state)
        idx = self.write_text(game_state)
        if self.current_interactable is not None:
            self.draw_portrait()
        if self.done_reading:
            return self.advance_to_next_node(idx, game_state)

    def advance_after_fight(self, game_state):
        # 0 is win, 1 is lose
        child_key = 0 if game_state.last_fight_won else 1
        self.tree = self.tree.children[child_key].children[0]
        game_state.fight_from_dialogue = False
        game_state.last_fight_won = None

    def advance_to_next_node(self, idx, game_state):
        if self.tree.jmp is not None:
            self.del_keys.append(self.tree.jmp)
            self.tree = self.trees[self.tree.jmp]
            return
        if self.tree.init_fight:
            self.done_reading = False
            game_state.fight_from_dialogue = True
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
        y = self.text_pos[1]
        x = self.text_pos[0]
        idx = 0
        for choices in self.tree.children:
            color = GREEN if idx == self.cursor_index else WHITE
            draw_text(choices.text, x, y, self.font_size, color)  # Adjusted X position
            y += 32
            idx += 1

    def make_choice(self, game_state):
        if is_key_pressed(KEY_ENTER):
            rel_mods = self.tree.children[self.cursor_index].rel_mods
            # there's a better way to do this
            for key, value in rel_mods.items():
                for friend in game_state.current_map.friends:
                    if friend.name == key:
                        self.showing_heart = True
                        self.heart_animation_start_time = get_time()
                        friend.rel += value
                        self.liked_choice = True if value > 0 else False
            self.done_reading = True
            return self.cursor_index

    # Write text and choices. Return 0 if no choice was made, otherwise return choice index
    def write_text(self, game_state):
        self.set_interactable(game_state, self.tree)
        # this will probably not work with multiple speakers
        if self.showing_heart:
            self.draw_heart(self.tree.speaker, self.liked_choice)
            if get_time() - self.heart_animation_start_time > 2:
                self.showing_heart = False
        pages = [self.tree.text[i:i + 64] for i in range(0, len(self.tree.text), 64)]
        if self.curr_page == len(pages) and len(self.tree.children) > 1 and not self.tree.auto_choice:
            self.write_choices()
            self.move_cursor_vertical(len(self.tree.children))
            return self.make_choice(game_state)

        elif self.curr_page >= len(pages):
            self.curr_page = 0
            self.done_reading = True
            return 0
        else:
            self.done_reading = False
        if self.current_interactable is not None:
            draw_text(self.current_interactable.name.upper(), self.name_pos[0], self.name_pos[1], self.font_size,SKYBLUE)
        else:
            draw_text("ME", self.name_pos[0], self.name_pos[1], 15, SKYBLUE)
        draw_text(pages[self.curr_page], self.text_pos[0], self.text_pos[1], self.font_size, WHITE)
        if is_key_pressed(KEY_ENTER):
            self.curr_page += 1
        return 0

    def set_interactable(self, game_state, tree):
        speaker = tree.speaker
        for friend in game_state.current_map.friends:
            if friend.name.lower() == speaker.lower():
                self.current_interactable = friend
                return
        self.current_interactable = None
        return

    def draw_portrait(self):
        origin = Vector2(0, 0)
        sub_texture = Rectangle(0, 0, 64, 64)
        scale = 2
        portrait_width = sub_texture.width * scale
        destination = Rectangle(self.portrait_pos[0], self.portrait_pos[1], sub_texture.width * scale,
                                sub_texture.height * scale)
        textures.load_texture(self.current_interactable.portrait)
        portrait_texture = textures.id_to_raylib(self.current_interactable.portrait)
        draw_texture_pro(portrait_texture, sub_texture, destination, origin, 0, WHITE)

    def write_nothing_say(self, game_state):
        self.draw_box()
        draw_text("There's nothing to talk about now", self.text_pos[0], self.text_pos[1], self.font_size, WHITE)
        if is_key_pressed(KEY_ENTER):
            game_state.pop_render_layer()

    def draw_scene(self, game_state):
        if self.background is not None:
            draw_texture(textures.id_to_raylib(self.background), 0, 0, WHITE)
        if self.tree.setup is not None:
            if self.tree.setup.render is not None:
                id = textures.load_texture('assets/backgrounds/' + self.tree.setup.render)
                self.background = id
            if self.tree.setup.stop_music:
                game_state.play_music(None)
            elif self.tree.setup.music is not None and game_state.music != self.tree.setup.music:
                game_state.play_music(self.tree.setup.music)
            if self.tree.setup.sound is not None:
                game_state.play_sound(self.tree.setup.sound)

        self.draw_box()

    def draw_text_with_border(self, text, x, y, text_color, border_color):
        offsets = [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]
        for offset in offsets:
            draw_text(text, x + offset[0], y + offset[1], self.font_size, border_color)

        draw_text(text, x, y, self.font_size, text_color)

    def draw_heart(self, name, liked):
        heart_texture = load_texture('assets/hearts.png')
        rl_texture = textures.id_to_raylib(heart_texture)

        if liked:
            sub_texture = Rectangle(0, 0, 32, 32)
            destination = Rectangle(32, 32, 32, 32)
            draw_texture_pro(rl_texture, sub_texture, destination, Vector2(0, 0), 0, WHITE)
        else:
            sub_texture = Rectangle(64, 96, 32, 32)
            destination = Rectangle(32, 32, 32, 32)
            draw_texture_pro(rl_texture, sub_texture, destination, Vector2(0, 0), 0, WHITE)

        self.draw_text_with_border(name, 64, 32, WHITE, BLACK)

    def draw_box(self):
        draw_rectangle(0, SCREEN_HEIGHT - 96, SCREEN_WIDTH, 96, BLACK)
