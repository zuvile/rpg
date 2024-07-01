import pyray as rl

# todo solve circular import when trying to import Object in collision.py
def blocked_by_object(obj, game_state, dx, dy):
    new_x = obj.rec.x + dx
    new_y = obj.rec.y + dy
    # is this really a good way to check for collision
    rec = rl.Rectangle(new_x, new_y, obj.size, obj.size)
    walls = game_state.map.walls
    for wall in walls:
        rl_wall_rec = rl.Rectangle(wall.rec.x, wall.rec.y, wall.rec.width, wall.rec.height)
        if rl.check_collision_recs(rec, rl_wall_rec):
            return True
    return False


def should_init_fight(player, game_state):
    map = game_state.map
    enemies = map.enemies
    for enemy in enemies:
        player_rl_rec = rl.Rectangle(player.rec.x, player.rec.y, player.size, player.size)
        enemy_rl_rec = rl.Rectangle(enemy.rec.x, enemy.rec.y, enemy.size, enemy.size)
        if rl.check_collision_recs(player_rl_rec, enemy_rl_rec):
            game_state.set_interactable(enemy)
            return True
    return False


def should_init_dialogue(player, game_state):
    map = game_state.map
    friends = map.friends
    for friend in friends:
        friend_rl_rec = rl.Rectangle(friend.rec.x, friend.rec.y, friend.size, friend.size)
        player_rl_rec = rl.Rectangle(player.rec.x, player.rec.y, player.size, player.size)
        if rl.check_collision_recs(player_rl_rec, friend_rl_rec):
            game_state.set_interactable(friend)
            return True
    return False


def off_the_window(obj, dx, dy):
    new_x = obj.rec.x + dx
    new_y = obj.rec.y + dy
    if 0 <= new_x <= (rl.get_screen_width() - obj.size) and 0 <= new_y <= (
            rl.get_screen_height() - obj.size):

        return False
    return True
