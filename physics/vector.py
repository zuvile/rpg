import pyray as rl
import math

def move_away(player, enemy, distance):
    vector1 = rl.Vector2(player.rec.x, player.rec.y)
    vector2 = rl.Vector2(enemy.rec.x, enemy.rec.y)

    direction_vector = rl.vector2_subtract(vector1, vector2)
    normalized = rl.vector2_normalize(direction_vector)
    scaled = rl.vector2_scale(normalized, distance)
    vector1 = rl.vector2_subtract(vector1, scaled)
    vector2 = rl.vector2_add(vector2, scaled)

    return vector1, vector2

def get_dist(player, enemy):
    vector1 = rl.Vector2(player.rec.x, player.rec.y)
    vector2 = rl.Vector2(enemy.rec.x, enemy.rec.y)

    direction_vector = rl.vector2_subtract(vector1, vector2)

    return math.ceil(rl.vector2_length(direction_vector) / 32)
