from scenarios.day_base import DayBase


class Day0(DayBase):
    def load_day(self, game_state):
        self.load_entities(game_state)
        self.load_dialogues(game_state)
        self.load_story(game_state)

    def load_entities(self, game_state):
        characters = game_state.characters
        for character in characters:
            if character.name == "Cassius":
                pass
                # todo set location

    def load_maps(self):
        pass

    def load_dialogues(self, game_state):
        for character in game_state.characters:
            if character.name == "Cassius":
                character.update_dialogue_trees("dialogue_files/cassius_dialogues.txt")

    def load_story(self, game_state):
        pass
