from cursor import Cursor
from pyray import *
from entities.card import CardType

class CardSelect(Cursor):
    def __init__(self):
        super().__init__()
        self.current_card = None
        self.player = None
        self.enemy = None
        self.done = False
        self.card_played = False
        self.is_moving = False
        self.is_healing = False
        self.is_attacking = False
        self.map_arr = [[0 for _ in range(19)] for _ in range(11)]
        self.game_state = None

    def enter(self, game_state):
        self.player = game_state.player
        self.enemy = game_state.get_interactable()
        self.game_state = game_state
        if self.cursor_point.x == 0 and self.cursor_point.y == 0:
            self.cursor_point = Vector2(self.player.rec.x, self.player.rec.y)

    def is_card_selected(self):
        return self.current_card is not None

    def play_card(self):
        card = self.player.deck.cards[self.cursor_index]
        if is_key_pressed(KEY_ENTER):
            self.current_card = card


    def draw(self):
        if self.card_played and not self.player.in_animation():
            self.done = True
            return

        self.draw_card_deck()
        #wait for animation to finish
        if self.card_played and self.player.in_animation():
            return

        if self.is_moving:
            self.handle_moving()
        elif self.is_healing:
            self.handle_healing()
        elif self.is_attacking:
            self.handle_attacking()
        else:
            self.move_cursor_horizontal(len(self.player.deck.cards))
            self.play_card()
            self.draw_selected_card()

            if self.current_card is None:
                return

            if self.current_card.type == CardType.HEAL:
                self.is_healing = True
            elif self.current_card.type == CardType.MOVE:
                self.is_moving = True
            elif self.current_card.type == CardType.ATTACK:
                self.is_attacking = True

    def handle_attacking(self):
        self.draw_grid()
        if is_key_pressed(KEY_ENTER):
            if self.map_arr[int(self.cursor_point.y) // 32][int(self.cursor_point.x) // 32] == 1 and self.enemy.rec.x == int(self.cursor_point.x) and self.enemy.rec.y == int(self.cursor_point.y):
                pts = self.player.do_attack()
                self.enemy.apply_damage(pts)
                self.is_attacking = False
                self.card_played = True
                self.game_state.add_to_log("You did " + str(pts) + " DMG")
            else:
                self.game_state.add_to_log("Invalid attack")

    def handle_healing(self):
        self.player.heal(self.current_card.heal)
        self.is_healing = False
        self.card_played = True
        self.game_state.add_to_log("You healed:" + str(self.current_card.heal) + " HP")

    def handle_moving(self):
        self.draw_grid()
        if is_key_pressed(KEY_ENTER):
            if self.map_arr[int(self.cursor_point.y) // 32][int(self.cursor_point.x) // 32] == 1:
                self.player.auto_move(self.cursor_point.x - self.player.rec.x, self.cursor_point.y - self.player.rec.y)
                self.is_moving = False
                self.card_played = True
                self.game_state.add_to_log("You moved.")
            else:
                self.game_state.add_to_log("Invalid move")

    def exit_state(self):
        self.current_card = None
        self.card_played = False
        self.done = False

    def draw_card_deck(self):
        x = 32
        y = 10*32

        for index, card in enumerate(self.player.deck.cards):
            colour = RED
            if self.cursor_index == index:
                colour = GREEN
            draw_rectangle(x + 32, y, 64, 64, colour)
            draw_text(card.name, x + 32, y, 20, BLACK)
            x += 62

    def draw_selected_card(self):
        curr_card = self.player.deck.cards[self.cursor_index]
        draw_rectangle(19*32, 10*32, 128, 192, GRAY)
        draw_text(curr_card.name, 20*32, 10*32, 20, BLACK)
        draw_text(curr_card.description, 19*32, 11*32, 16, BLACK)

    def draw_grid(self):
        semi_transparent_red = Color(255, 0, 0, 128)
        player_tile_x = self.player.rec.x // 32
        player_tile_y = self.player.rec.y // 32
        for row_index in range(len(self.map_arr)):
            for tile_index in range(len(self.map_arr[row_index])):
                if player_tile_x - self.current_card.range <= tile_index <= player_tile_x + self.current_card.range and \
                        player_tile_y - self.current_card.range <= row_index <= player_tile_y + self.current_card.range:
                    self.map_arr[row_index][tile_index] = 1
                else:
                    self.map_arr[row_index][tile_index] = 0

        for row_index in range(len(self.map_arr)):
            for tile_index in range(len(self.map_arr[row_index])):
                if self.map_arr[row_index][tile_index] == 1:
                    draw_rectangle(tile_index * 32, row_index * 32, 32, 32, semi_transparent_red)

        semi_transparent_green = Color(0, 255, 0, 128)
        self.move_omnidirectional(self.cursor_point.x, self.cursor_point.y, self.map_arr)
        origin = Vector2(0, 0)
        cursor_rect = Rectangle(self.cursor_point.x, self.cursor_point.y, 32, 32)
        draw_rectangle_pro(cursor_rect,  origin, 0, semi_transparent_green)