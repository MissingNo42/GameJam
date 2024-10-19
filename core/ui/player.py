from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.properties import NumericProperty, BooleanProperty, ObjectProperty
from kivy.uix.image import Image

from .theme import Theme

__all__ = (
    "Player",
)


class Player(Image, Theme):
    FPS = 30
    ACCEL_X = 2000 / FPS
    ACCEL_Y = 2000 / FPS
    MAX_SPEED_X = 1.5 / FPS
    MAX_SPEED_Y = 2 / FPS

    accel_x = NumericProperty(0)
    accel_y = NumericProperty(0)

    speed_x = NumericProperty(0)
    speed_y = NumericProperty(0)

    ipos_x = NumericProperty(0)
    pos_x = NumericProperty(0)
    pos_y = NumericProperty(0)

    physic_running = BooleanProperty(True)

    move_right = BooleanProperty(False)
    move_left = BooleanProperty(False)
    jump = BooleanProperty(False)

    factor = NumericProperty(0)

    def __init__(self, **kwargs):
        src = f"{self.theme}/player.gif"
        super().__init__(source=src, **kwargs)

        self.pos_x = self.ipos_x
        self.render()

        Clock.schedule_interval(self.run_physic, 1 / self.FPS)

    def on_factor(self, instance, value):
        self.size = (self.factor, self.factor)
        self.render()

    def on_ipos_x(self, instance, value):
        self.pos_x = self.ipos_x
        self.render()

    def render(self):
        self.x = self.factor * self.ipos_x
        self.y = self.factor * self.pos_y

    def on_pos_y(self, instance, value):
        self.y = self.factor * self.pos_y

    def run_physic(self, dt):
        if self.physic_running:

            if self.move_right:
                self.accel_x = self.ACCEL_X
            elif self.move_left:
                self.accel_x = -self.ACCEL_X
            else:
                self.accel_x = 0

            if self.jump:
                self.accel_y = self.ACCEL_Y
            else:
                self.accel_y = 0

            sx = self.speed_x + self.accel_x
            sy = self.speed_y + self.accel_y

            self.speed_x = max(-self.MAX_SPEED_X, min(self.MAX_SPEED_X, sx))
            self.speed_y = max(-self.MAX_SPEED_Y, min(self.MAX_SPEED_Y, sy))

            self.pos_x += self.speed_x
            self.pos_y += self.speed_y

            self.accel_x = 0
            self.accel_y = 0

    def on_theme(self, instance, value):
        super().on_theme(instance, value)
        self.source = f"{self.theme}/{self.source}"

    def on_texture(self, instance, value):
        self.config_texture(False)

    def on_size(self, instance, value):
        self.config_texture()

    def config_texture(self, tex: bool = True):
        self.texture: Texture

        if not self.texture:
            return

        self.texture.min_filter = 'nearest'
        self.texture.mag_filter = 'nearest'

