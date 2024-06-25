from pyray import *
from actions import *

from player import Player
from enemy import Enemy
from wall import Wall

init_window(800, 480, "Game")
set_target_fps(60)
player = Player(3 * 32, 3 * 32)
is_fighting = False
map = {
    'walls': [],
    'enemies': []
}

def add_enemies():
    map['enemies'].append(Enemy(5 * 32, 5 * 32))

add_enemies()

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

def move():
    if is_key_down(KEY_W):
        return player.move(0, -2, map)
    if is_key_down(KEY_S):
        return player.move(0, 2, map)
    if is_key_down(KEY_A):
        return player.move(-2, 0, map)
    if is_key_down(KEY_D):
        return player.move(2, 0, map)


map_texture = load_texture('assets/tiled_map.png')
fight_texture = load_texture('assets/fight.png')
add_walls()

while not window_should_close():
    begin_drawing()
    if is_fighting:
        draw_texture(fight_texture, 0, 0, WHITE)
        player.draw()
        for enemy in map['enemies']:
            enemy.draw()
        draw_text("FIGHT", 640, 64, 20, RED)
        mouse_point = get_mouse_position()
        if check_collision_point_rec(mouse_point, Rectangle(640, 64, 128, 64)):
            draw_text("FIGHT", 640, 64, 20, GREEN)
            if is_mouse_button_down(MOUSE_LEFT_BUTTON):
                draw_text("ATTACKING ENEMY", 32, 32, 20, RED)
        if is_key_down(KEY_SPACE):
            is_fighting = False
    else:
        draw_texture(map_texture, 0, 0, WHITE)
        for wall in map['walls']:
            wall.draw()
        for enemy in map['enemies']:
            enemy.draw()
        action = move()
        if action == Actions.FIGHT:
            is_fighting = True
        player.draw()
    end_drawing()
close_window()


