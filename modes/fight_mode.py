from modes.game_mode import GameMode
from pyray import *
from cursor import Cursor
from spell import get_spells

class FightMode(GameMode, Cursor):
    def __init__(self):
        super().__init__()
        self.end_of_fight = False
        self.message = "You are in a fight!"
        self.final_message = ""
        self.texture = load_texture('assets/fight.png')
        self.show_spell_menu = False
        self.is_enemy_turn = False
        self.start_of_fight = True
        self.last_fight_won = None

    def draw(self, game_state):
        draw_texture(self.texture, 0, 0, WHITE)
        player = game_state.player
        player.draw()
        enemy = game_state.get_interactable()
        enemy.draw()

        if not game_state.is_layer_top(self):
            return

        if self.end_of_fight:
            draw_text(self.final_message, 2 * 32, 10 * 32, 32, GREEN)
            if is_key_pressed(KEY_ENTER):
                self.end_of_fight = False
                game_state.pop_render_layer()
        if self.show_spell_menu:
            spells = get_spells(player.magic)
            options = [spell.name for spell in spells]
            options.append("BACK")
            if is_key_pressed(KEY_ENTER):
                if options[self.cursor_index] == "BACK":
                    self.show_spell_menu = False
                else:
                    self.player_spell(spells[self.cursor_index], player, enemy)
        else:
            options = ["ATTACK", "SPELL"]
            if is_key_pressed(KEY_ENTER) and options[self.cursor_index] == "ATTACK":
                self.player_attack(player, enemy)
            if is_key_pressed(KEY_ENTER) and options[self.cursor_index] == "SPELL":
                self.show_spell_menu = True

        self.draw_ui(player, enemy, options)
        if self.start_of_fight:
            self.jump_back(player, enemy)
            self.start_of_fight = False
            enemy.draw()
            player.draw()
        self.move_cursor(len(options))

        if not enemy.is_alive():
            self.final_message = "You won the fight!"
            game_state.last_fight_won = True
            self.end_of_fight = True
        elif self.is_enemy_turn and is_key_pressed(KEY_ENTER):
            self.enemy_turn(player, enemy, game_state)

    def player_spell(self, spell, player, enemy):
        if player.mana >= spell.mana_cost:
            player.mana -= spell.mana_cost
            player.hp += spell.heal
            player.mana += spell.mana_gain
            dmg = spell.damage
            self.message = "You cast " + spell.name
            enemy.apply_damage(dmg)
            self.is_enemy_turn = True
        else:
            self.message = "Not enough mana"

    def enemy_turn(self, player, enemy, game_state):
        dmg = enemy.do_attack()
        self.message = "Enemy attacked for " + str(dmg) + " damage"
        draw_text(self.message, 2 * 32, 14 * 32, 32, RED)
        player.apply_damage(dmg)
        if not player.is_alive():
            game_state.last_fight_won = False
            self.final_message = "You lost the fight!"
            self.end_of_fight = True

    def player_attack(self, player, enemy):
        dmg = player.do_attack()
        self.message = "You attacked for " + str(dmg) + " damage"
        draw_text(self.message, 2 * 32, 14 * 32, 32, RED)
        enemy.apply_damage(dmg)
        self.is_enemy_turn = True

    def draw_ui(self, player, enemy, options):
        x = 640
        y = 65

        for index, option in enumerate(options):
            colour = RED
            if self.cursor_index == index:
                colour = GREEN
            draw_text(option, x, y, 20, colour)
            y += 32
        draw_text("Player HP: " + str(player.hp), 2 * 32, 11 * 32, 16, RED)
        draw_text("Enemy HP: " + str(enemy.hp), 2 * 32, 12 * 32, 16, RED)
        draw_text("Player mana: " + str(player.mana), 2 * 32, 13 * 32, 16, RED)
        draw_text(self.message, 2 * 32, 14 * 32, 14, RED)

    def jump_back(self, player, enemy):
        player.rec.x = player.rec.x - 32
        player.rec.y = player.rec.y - 32
        enemy.rec.x = enemy.rec.x + 32
        enemy.rec.y = enemy.rec.y + 32

    def prepare_new_fight(self):
        self.end_of_fight = False
        self.message = "You are in a fight!"
        self.final_message = ""
        self.show_spell_menu = False
        self.is_enemy_turn = False
        self.start_of_fight = True
