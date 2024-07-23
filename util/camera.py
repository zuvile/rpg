from pyray import *


class Camera:
    def __init__(self):
        self.camera = Camera2D()
        self.camera.target = Vector2(0, 0)
        self.camera.offset = Vector2(get_screen_width() / 2, get_screen_height() / 2)
        self.camera.rotation = 0.0
        self.camera.zoom = 2.0

    def begin(self):
        begin_mode_2d(self.camera)

    def set_target(self, target: Vector2):
        self.camera.target = target

    def set_zoom(self, zoom):
        self.camera.zoom = zoom

    def set_offset(self, offset: Vector2):
        self.set_offset(offset)
