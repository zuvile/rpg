from pyray import *
import random

class Camera:
    def __init__(self):
        self.camera = Camera2D()
        self.camera.target = Vector2(0, 0)
        self.camera.offset = Vector2(get_screen_width() / 2, get_screen_height() / 2)
        self.camera.rotation = 0.0
        self.camera.zoom = 2.0
        self.shake_animation_start = 0
        self.is_shaking = False

    def update(self):
      pass

    def begin(self):
        begin_mode_2d(self.camera)

    def begin_fight_cam(self):
        self.camera = Camera2D()
        self.camera.target = Vector2(0, 0)
        self.camera.offset = Vector2(0, 0)
        self.camera.rotation = 0.0
        self.camera.zoom = 1.0

        if self.is_shaking:
            self.camera.offset.x += random.uniform(-3, 3) * self.camera.zoom
            self.camera.offset.y += random.uniform(-3, 3) * self.camera.zoom
            if get_time() - self.shake_animation_start > 1:
                self.is_shaking = False

        begin_mode_2d(self.camera)

    def end(self):
        end_mode_2d()

    def set_target(self, target: Vector2):
        self.camera.target = target

    def set_zoom(self, zoom):
        self.camera.zoom = zoom

    def set_offset(self, offset: Vector2):
        self.set_offset(offset)

    def shake(self):
        self.is_shaking = True
        self.shake_animation_start = get_time()

    def __repr__(self):
        return f"Camera({self.camera.offset.x},{self.camera.offset.y})"

    def reset(self):
        self.camera = Camera2D()
        self.camera.target = Vector2(0, 0)
        self.camera.offset = Vector2(get_screen_width() / 2, get_screen_height() / 2)
        self.camera.rotation = 0.0
        self.camera.zoom = 2.0
        self.shake_animation_start = 0
        self.is_shaking = False
