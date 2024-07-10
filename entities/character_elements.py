import pyray as rl
import math

def draw_health_bar(color, character):
    border_thickness = 1
    hp = math.ceil(32 / character.max_hp * character.hp)
    x = int(character.rec.x) - border_thickness
    y = int(character.rec.y) - 8 - border_thickness
    width = 32 + border_thickness * 2
    height = 8 + border_thickness * 2
    rl.draw_rectangle(x, y, width, height, rl.BLACK)
    rl.draw_rectangle(x + border_thickness, y + border_thickness, 32, 8, rl.WHITE)
    rl.draw_rectangle(x + border_thickness, y + border_thickness, hp, 8, color)