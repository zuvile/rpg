from pyray import *

from character import Character
from wall import Wall

init_window(900, 540, "Game")
set_target_fps(60)
player = Character(0,0)
map = {
    'walls': []
}

map_texture = load_texture('assets/tiled_map.png')

def add_walls():
    y = 0
    lines = open('assets/tiled_map_trees.csv', 'r').readlines()
    for line in lines:
        x = 0
        for char in line.split(','):
            if char != '-1':
                map['walls'].append(Wall(x * 32, y * 32))
            x += 1
        y += 1


while not window_should_close():
    begin_drawing()
    add_walls()
    draw_texture(map_texture, 0, 0, WHITE)
    for wall in map['walls']:
        wall.draw()
    if is_key_down(KEY_W):
        player.move(0, -2, map)
    if is_key_down(KEY_S):
        player.move(0, 2, map)
    if is_key_down(KEY_A):
        player.move(-2, 0, map)
    if is_key_down(KEY_D):
        player.move(2, 0, map)
    player.draw()
    end_drawing()
close_window()


