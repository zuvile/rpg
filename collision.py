from pyray import *


# todo solve circular import when trying to import Object in collision.py
def blocked_by_object(obj, map, dx, dy):
    new_x = obj.rec.x + dx
    new_y = obj.rec.y + dy
    # is this really a good way to check for collision
    rec = Rectangle(new_x, new_y, obj.size, obj.size)
    walls = map['walls']
    for wall in walls:
        if check_collision_recs(rec, wall.rec):
            return True
    return False


def should_init_fight(player, map):
    enemies = map['enemies']
    for enemy in enemies:
        if check_collision_recs(player.rec, enemy.rec):
            return True


def off_the_window(obj, dx, dy):
    new_x = obj.rec.x + dx
    new_y = obj.rec.y + dy
    if 0 <= new_x <= (get_screen_width() - obj.size) and 0 <= new_y <= (
            get_screen_height() - obj.size):

        return False
    return True
