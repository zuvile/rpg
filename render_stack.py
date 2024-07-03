class RenderStack:
    def __init__(self, game_state):
        self._stack = []
        self.game_state = game_state

    def push(self, renderable):
        self._stack.append(renderable)

    def pop(self):
        return self._stack.pop()

    def render(self):
        for renderable in self._stack:
            renderable.draw(self.game_state)

    def is_layer_top(self, layer):
        return self._stack[-1] == layer
