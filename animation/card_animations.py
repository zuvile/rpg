from animation.animation import Animation
from pytweening import easeInOutSine


class FlashAnimation(Animation):
    def __init__(self):
        super().__init__(True, 1)
        self.func = lambda t: (t * 100 // 20) % 2


class MoveAnimation(Animation):
    def __init__(self):
        super().__init__(False, 0.5)
        self.func = lambda t: easeInOutSine(t)
        self.pause = 1

    def eval(self, t):
        if self.start_time is None:
            return 0
        if self.start_time + self.duration < t < self.start_time + self.duration + self.pause:
            return 1
        if t > self.start_time + self.duration:
            return 0
        return self.func((t - self.start_time) / self.duration)
