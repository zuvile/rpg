from entities.rectangle import Rectangle
from collision import off_the_window, blocked_by_object

# base class for any object
class Entity:
    def __init__(self, x, y, size):
        self.size = size
        self.rec = Rectangle(x, y, size, size)
            
    def can_move(self, dx, dy, game_state):
        if off_the_window(self, dx, dy) or blocked_by_object(self, game_state, dx, dy):
            return False
        return True
