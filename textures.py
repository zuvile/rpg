import pyray as rl

game_textures = {}

def load_texture(file_name):
    if file_name not in game_textures:
        game_textures[file_name] = rl.load_texture(file_name)
    return file_name

def id_to_raylib(id):
    return game_textures[id]
