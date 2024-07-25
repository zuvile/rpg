from entities.character import Character
from typing import Optional
from dialogue.dialogue import Dialogue
from render_stack import RenderStack
from modes.dialogue_mode import DialogueMode
from modes.fight_mode import FightMode
from modes.story_mode import StoryMode
from modes.explore_mode import ExploreMode
from maps.map import MapType
from scenarios.load_scenario import load_scenario
from pyray import *
from util.camera import Camera



class GameState:
    def __init__(self, player, maps, characters):
        self.player = player
        self.interacting_with: Optional[Character] = None
        self.dialogue = Dialogue()
        self.day = -1
        self._render_stack = RenderStack(self)
        self.dialogue_mode = DialogueMode()
        self.story_mode = StoryMode()
        self.explore_mode = ExploreMode()
        self.last_fight_won = None
        self.fight_from_dialogue = False
        self._log = []
        self._maps = maps
        self.characters = characters
        self.current_map = self._maps[MapType.CASTLE_GROUNDS]
        self.music = None
        self.sound_effect = None
        self.stop_music = False
        self.music_stream = None
        self.sound = None
        self.camera = Camera()


    def set_interactable(self, character: Character):
        self.interacting_with = character

    def clear_interactable(self):
        self.interacting_with = None

    def get_interactable(self):
        return self.interacting_with

    def advance_day(self):
        self.day += 1
        load_scenario(self)

    def push_fight_mode(self):
        #fight mode needs to be created each time to reset the fight
        new_fight_mode = FightMode()
        self._render_stack.push(new_fight_mode)

    def push_new_explore_mode(self):
        self._render_stack.push(self.explore_mode)

    def push_new_story_mode(self):
        self._render_stack.push(self.story_mode)

    def push_new_dialogue_mode(self):
        self._render_stack.push(self.dialogue_mode)

    def render(self):
        self._render_stack.render()

    def is_layer_top(self, layer):
        return self._render_stack.is_layer_top(layer)

    def pop_render_layer(self):
        self._render_stack.pop()

    def add_to_log(self, message):
        self._log.append(message)
        if len(self._log) > 10:
            self._log.pop(0)

    def get_log(self):
        return self._log[-5:][::-1]

    def play_music(self, music):
        if music is None and self.music_stream is not None:
            stop_music_stream(self.music_stream)
            unload_music_stream(self.music_stream)
            self.music_stream = None
        elif self.music != music:
            self.music_stream = load_music_stream('sounds/' + music)
            play_music_stream(self.music_stream)
        self.music = music

    def play_sound(self, sound):
        if sound is not None and self.sound != sound:
            self.sound_effect = load_sound('sounds/' + sound)
            play_sound(self.sound_effect)
        self.sound = sound

    def play_rep_sound(self, sound):
        if sound is not None and self.sound != sound:
            self.sound_effect = load_sound('sounds/' + sound)
        if self.sound_effect is not None and not is_sound_playing(self.sound_effect):
            play_sound(self.sound_effect)
        self.sound = sound

    def update(self):
        self.current_map.update(self.characters)
        if self.music_stream is not None:
            update_music_stream(self.music_stream)
        self.camera.update()
        # if self.sound:
        #     update_sound(self.sound)
        # update_sound(self.sound, )


