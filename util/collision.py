import pyray as rl

def blocked_by_object(obj, game_state, dx, dy):
    new_x = obj.rec.x + dx
    new_y = obj.rec.y + dy
    rec = rl.Rectangle(new_x, new_y, obj.size, obj.size)
    walls = game_state.current_map.walls
    for wall in walls:
        rl_wall_rec = rl.Rectangle(wall.rec.x, wall.rec.y, wall.rec.width, wall.rec.height)
        if rl.check_collision_recs(rec, rl_wall_rec):
            return True
    return False


def should_init_fight(player, game_state):
    map = game_state.current_map
    enemies = map.enemies
    for enemy in enemies:
        player_rl_rec = rl.Rectangle(player.rec.x, player.rec.y, 32, 32)
        enemy_rl_rec = rl.Rectangle(enemy.rec.x, enemy.rec.y, 32, 32)
        if rl.check_collision_recs(player_rl_rec, enemy_rl_rec):
            game_state.set_interactable(enemy)
            return True
    return False


def should_init_dialogue(player, game_state):
    map = game_state.current_map
    friends = map.friends
    for friend in friends:
        friend_rl_rec = rl.Rectangle(friend.rec.x, friend.rec.y, 32, 32)
        player_rl_rec = rl.Rectangle(player.rec.x, player.rec.y, 32, 32)
        if rl.check_collision_recs(player_rl_rec, friend_rl_rec):
            game_state.set_interactable(friend)
            return True
    return False


def off_the_window(obj, dx, dy, map):
    #todo map widh
    new_x = obj.rec.x + dx
    new_y = obj.rec.y + dy
    rect = rl.Rectangle(0, 0, map.width, map.height)
    point = rl.Vector2(new_x, new_y)
    return not rl.check_collision_point_rec(point, rect)
