class Animation():
    def __init__(self, repeating, duration):
        self.repeating = repeating
        self.start_time = None
        self.duration = duration
        self.func = lambda t: (t * 100 // 20) % 2

    def eval(self, t):
        if self.start_time is None or self.finished(t):
            return 0

        return self.func(t - self.start_time)

    def start(self, t):
        self.start_time = t

    def finished(self, t):
        print('start time' + str(self.start_time))
        # print('duration' + str(self.duration))
        print('t' + str(t))
        if self.start_time is None or self.duration is None:
            return True
        return (t - self.start_time) >= self.duration
