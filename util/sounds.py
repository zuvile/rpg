import pyray as rl

curr_sound = None
game_sounds = {}
music = None
music_stream = None


def load_sound(file_name):
    if file_name not in game_sounds:
        game_sounds[file_name] = rl.load_sound(file_name)
    return game_sounds[file_name]


def play_sound(file_name):
    global curr_sound

    if curr_sound is not None and rl.is_sound_playing(curr_sound):
        return

    file_name = 'sounds/' + file_name
    sound = load_sound(file_name)
    curr_sound = sound
    rl.play_sound(sound)


def play_music(music):
    global music_stream
    if music_stream is None:
        music_stream = rl.load_music_stream('sounds/' + music)
    rl.play_music_stream(music_stream)


def stop_music():
    global music_stream
    if music_stream is not None:
        rl.stop_music_stream(music_stream)
        music_stream = None
def stop_sound():
    global curr_sound
    if curr_sound is not None:
        rl.stop_sound(curr_sound)

def update_music():
    global music_stream
    if music_stream is not None:
        rl.update_music_stream(music_stream)
