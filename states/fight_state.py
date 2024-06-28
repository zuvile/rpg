from states.game_state import GameState
from pyray import *
from actions import *
from cursor import Cursor

class FightState(GameState, Cursor):
    def __init__(self):
        self.end_of_fight = False
        self.message = "You are in a fight!"
        self.final_message = ""
        self.texture = load_texture('assets/fight.png')

    def draw(self, player, map):
        draw_texture(self.texture, 0, 0, WHITE)
        player.draw()
        enemy = map.enemies[0]
        enemy.draw()

        if self.end_of_fight:
            draw_text(self.final_message, 2 * 32, 10 * 32, 32, GREEN)
            if is_key_pressed(KEY_ENTER):
                self.end_of_fight = False
                return Actions.EXPLORE

        options = ["ATTACK", "SPELL", "RUN AWAY"]
        self.draw_ui(player, enemy, options)
        self.move_cursor(len(options))

        if is_key_pressed(KEY_ENTER) and options[self.cursor_index] == "ATTACK":
            self.handle_attack(player, enemy)

        return Actions.FIGHT

    def handle_attack(self, player, enemy):
        dmg = player.do_attack()
        self.message = "You attacked for " + str(dmg) + " damage"
        draw_text(self.message, 2 * 32, 14 * 32, 32, RED)
        enemy.apply_damage(dmg)
        if not enemy.is_alive():
            self.final_message = "You won the fight!"
            self.end_of_fight = True
        else:
            dmg = enemy.do_attack()
            self.message = "Enemy attacked for " + str(dmg) + " damage"
            draw_text(self.message, 2 * 32, 14 * 32, 32, RED)
            player.apply_damage(dmg)
            if not player.is_alive():
                self.final_message = "You lost the fight!"
                self.end_of_fight = True

    def draw_ui(self, player, enemy, options):
        x = 640
        y = 65

        for index, option in enumerate(options):
            colour = RED
            if self.cursor_index == index:
                colour = GREEN
            draw_text(option, x, y, 20, colour)
            y += 32
        draw_text("Player HP: " + str(player.hp), 2 * 32, 12 * 32, 32, RED)
        draw_text("Enemy HP: " + str(enemy.hp), 2 * 32, 13 * 32, 32, RED)
        draw_text(self.message, 2 * 32, 14 * 32, 32, RED)

