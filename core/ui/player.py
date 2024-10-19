from kivy.clock import Clock
from kivy.properties import NumericProperty, BooleanProperty, ObjectProperty
from kivy.uix.image import Image

from .theme import Theme

__all__ = (
    "Player",
)


class Player(Image, Theme):
    ACCEL_FACTOR = .05

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

        self.ipos_x = self.pos_x
        self.x = self.factor * self.ipos_x
        self.y = self.factor * self.pos_y

        Clock.schedule_once(self.run_physic, 0)

    def on_factor(self, instance, value):
        self.x = self.factor * self.ipos_x
        self.y = self.factor * self.pos_y
        self.size = (self.factor, self.factor)

    def on_pos_y(self, instance, value):
        self.y = self.factor * self.pos_y

    def run_physic(self, dt):
        if self.physic_running:

            if self.move_right:
                self.accel_x = self.ACCEL_FACTOR
            elif self.move_left:
                self.accel_x = -self.ACCEL_FACTOR
            else:
                self.accel_x = 0

            if self.jump:
                self.accel_y = self.ACCEL_FACTOR
            else:
                self.accel_y = 0

            self.speed_x += self.accel_x
            self.speed_y += self.accel_y

            self.pos_x += self.speed_x
            self.pos_y += self.speed_y

            self.accel_x = 0
            self.accel_y = 0

        Clock.schedule_once(self.run_physic, 0)

    def on_theme(self, instance, value):
        super().on_theme(instance, value)
        self.source = f"{self.theme}/{self.source}"
