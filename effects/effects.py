import pyray as rl
from util.sounds import play_sound

class Effects:
    def __init__(self):
        self._tint_start_time = 0
        self._in_tint = False
        self._tint_color = rl.WHITE
        self.curr_sound_name = None
        self.curr_sound = None

    def tint_view(self, colour):
        if not self._in_tint:
            self._in_tint = True
            self._tint_start_time = rl.get_time()
            self._tint_color = colour

    def shake_cam(self, camera):
        play_sound('debuff.wav')
        camera.shake()

    def get_color(self):
        if self._in_tint:
            if rl.get_time() - self._tint_start_time > 1:
                print(rl.get_time() - self._tint_start_time)
                self._in_tint = False
                return rl.WHITE
            else:
                return rl.RED
        else:
            return rl.WHITE
