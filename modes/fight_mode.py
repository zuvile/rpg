from modes.game_mode import GameMode
from pyray import *
from cursor import Cursor
from entities.card import CardType
from fight_map import FightMap

class FightMode(GameMode, Cursor):
    def __init__(self):
        super().__init__()
        self.end_of_fight = False
        self.texture = load_texture('assets/maps/fight_map.png')
        self.show_spell_menu = False
        self.is_enemy_turn = False
        self.start_of_fight = True
        self.last_fight_won = None
        self.message_stack = []
        self.player_orig_pos = None
        self.enemy_orig_pos = None
        self.last_card_used = None
        self.is_player_turn = True
        #todo a better name?
        self.detail_mode = False
        self.fight_map = FightMap()

        #map array pf 10x18
        self.map_arr = [[0 for _ in range(19)] for _ in range(11)]

    def draw(self, game_state):
        if not game_state.is_layer_top(self):
            return

        #todo debugging only
        game_state.map = self.fight_map
        self.fight_map.add_enemy(game_state.get_interactable())

        draw_rectangle(0, 0, 800, 480, WHITE)
        draw_texture(self.texture, 0, 0, WHITE)
        player = game_state.player
        if self.start_of_fight:
            self.assume_start_pos(player, game_state.get_interactable())
            self.start_of_fight = False
        player.draw()
        enemy = game_state.get_interactable()
        enemy.draw()
        self.draw_selected_card(player)
        self.draw_fight_messages()

        if self.end_of_fight:
            if is_key_pressed(KEY_ENTER):
                self.end_of_fight = False
                game_state.pop_render_layer()
                return

        self.draw_ui(player, enemy)
        self.draw_card_deck(player)

        if not self.detail_mode:
            self.move_cursor_horizontal(len(player.deck.cards))

        self.play_card(player, enemy)
        self.draw_last_selected_card_effects(player, game_state)

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
            self.last_card_used = card
            self.detail_mode = True
            # if card.range > v.get_dist(player, enemy):
            #     self.message_stack.append("The enemy is too far away!")
            #     return
            # else:
            #     card.use(player, enemy)
            #     self.message_stack.append("You used " + card.name + "!")
            #     self.is_enemy_turn = True

    def draw_last_selected_card_effects(self, player, game_state):
        card = self.last_card_used
        if card is None:
            return
        semi_transparent_red = Color(255, 0, 0, 128)
        semi_transparent_green = Color(0, 255, 0, 128)
        if card.type == CardType.MOVE:
            player_tile_x = player.rec.x // 32
            player_tile_y = player.rec.y // 32
            for row_index in range(len(self.map_arr)):
                for tile_index in range(len(self.map_arr[row_index])):
                    if player_tile_x - card.range <= tile_index <= player_tile_x + card.range and \
                            player_tile_y - card.range <= row_index <= player_tile_y + card.range:
                        self.map_arr[row_index][tile_index] = 1

        for row_index in range(len(self.map_arr)):
            for tile_index in range(len(self.map_arr[row_index])):
                if self.map_arr[row_index][tile_index] == 1:
                    draw_rectangle(tile_index * 32, row_index * 32, 32, 32, semi_transparent_red)

        self.move_omnidirectional(self.cursor_point.x, self.cursor_point.y, self.map_arr)
        origin = Vector2(0, 0)
        cursor_rect = Rectangle(self.cursor_point.x, self.cursor_point.y, 32, 32)
        draw_rectangle_pro(cursor_rect,  origin, 0, semi_transparent_green)
        if is_key_pressed(KEY_ENTER):
            player.rec.x = self.cursor_point.x
            player.rec.y = self.cursor_point.y
            self.detail_mode = False
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
        y = 10*32

        for index, card in enumerate(player.deck.cards):
            colour = RED
            if self.cursor_index == index:
                colour = GREEN
            draw_rectangle(x + 32, y, 64, 64, colour)
            draw_text(card.name, x + 32, y, 20, BLACK)
            x += 62

    def assume_start_pos(self, player, enemy):
        #todo save prev pos
        player.rec.x = 1 * 32
        player.rec.y = 1 * 32

        enemy.rec.x = 4 * 32
        enemy.rec.y = 3 * 32

    def prepare_new_fight(self):
        self.end_of_fight = False
        self.message_stack = []
        self.show_spell_menu = False
        self.is_enemy_turn = False
        self.start_of_fight = True
        self.player_orig_pos = None
        self.enemy_orig_pos = None

    def draw_selected_card(self, player):
        curr_card = player.deck.cards[self.cursor_index]
        draw_rectangle(19*32, 10*32, 128, 192, GRAY)
        draw_text(curr_card.name, 20*32, 10*32, 20, BLACK)
        draw_text(curr_card.description, 19*32, 11*32, 16, BLACK)