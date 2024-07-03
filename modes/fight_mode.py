from modes.game_mode import GameMode
from pyray import *
from cursor import Cursor

class FightMode(GameMode, Cursor):
    def __init__(self):
        super().__init__()
        self.end_of_fight = False
        self.texture = load_texture('assets/fight.png')
        self.show_spell_menu = False
        self.is_enemy_turn = False
        self.start_of_fight = True
        self.last_fight_won = None
        self.message_stack = []

    def draw(self, game_state):
        draw_texture(self.texture, 0, 0, WHITE)
        player = game_state.player
        player.draw()
        enemy = game_state.get_interactable()
        enemy.draw()
        self.draw_fight_messages()

        if not game_state.is_layer_top(self):
            return

        if self.end_of_fight:
            if is_key_pressed(KEY_ENTER):
                self.end_of_fight = False
                game_state.pop_render_layer()
                return

        self.draw_ui(player, enemy)
        self.draw_card_deck(player)

        self.move_cursor_horizontal(len(player.deck.cards))
        self.play_card(player, enemy)

        if not enemy.is_alive():
            self.message_stack.append("You won the fight!")
            game_state.last_fight_won = True
            self.end_of_fight = True
        elif self.is_enemy_turn:
            self.enemy_turn(player, enemy, game_state)
            self.is_enemy_turn = False

    def play_card(self, player, enemy):
        card = player.deck.cards[self.cursor_index]
        if is_key_pressed(KEY_ENTER):
            card.use(player, enemy)
            self.message_stack.append("You used " + card.name + "!")
            self.is_enemy_turn = True

    def enemy_turn(self, player, enemy, game_state):
        dmg = enemy.do_attack()
        player.apply_damage(dmg)
        self.message_stack.append("The enemy did " + str(dmg) + " damage to you!")
        if not player.is_alive():
            game_state.last_fight_won = False
            self.message_stack.append("You lost the fight!")
            self.end_of_fight = True

    def draw_ui(self, player, enemy):
        draw_rectangle(19*32, 0, 10*32, 10*32, WHITE)
        draw_text("HP: " + str(player.hp), 20*32, 1*32, 16, BLACK)
        draw_text("Mana: " + str(player.mana), 20*32, 3*32, 16, BLACK)
        draw_text("Enemy HP: " + str(enemy.hp), 20*32, 2*32, 16, BLACK)

    def draw_fight_messages(self):
        y = 4*32
        for message in self.message_stack:
            draw_text(message, 10*32, y, 16, BLACK)
            y += 32

    def draw_card_deck(self, player):
        x = 32
        y = 300

        for index, card in enumerate(player.deck.cards):
            colour = RED
            if self.cursor_index == index:
                colour = GREEN
            draw_rectangle(x + 32, y, 64, 64, colour)
            draw_text(card.name, x + 32, y, 20, BLACK)
            x += 62

    def prepare_new_fight(self):
        self.end_of_fight = False
        self.message_stack = []
        self.show_spell_menu = False
        self.is_enemy_turn = False
        self.start_of_fight = True
