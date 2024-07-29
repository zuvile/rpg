from abc import ABC

class Animation(ABC):
    def __init__(self, repeating, duration):
        self.repeating = repeating
        self.start_time = None
        self.duration = duration
        self.func = None


    def eval(self, t):
        if self.start_time is None or self.finished(t):
            return 0
        return self.func(t - self.start_time)

    def start(self, t):
        self.start_time = t

    def finished(self, t):
        if self.start_time is None or self.duration is None:
            return True
        return (t - self.start_time) >= self.duration
