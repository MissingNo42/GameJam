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

    ACCEL_X = 5 / FPS
    ACCEL_Y = 5 / FPS

    MAX_SPEED_X = 1.5 / FPS
    MAX_SPEED_Y = 2 / FPS

    MIN_SPEED_X = 0.01
    MIN_SPEED_Y = 0.01

    SPEED_ATT_X = 0.80

    accel_x = NumericProperty(0)
    accel_y = NumericProperty(0)

    speed_x = NumericProperty(0)
    speed_y = NumericProperty(0)

    ipos_x = NumericProperty(0)
    ipos_y = NumericProperty(0)

    pos_x = NumericProperty(0)
    pos_y = NumericProperty(0)

    physic_running = BooleanProperty(True)

    move_right = BooleanProperty(False)
    move_left = BooleanProperty(False)
    jump = BooleanProperty(False)

    factor = NumericProperty(0)

    DEADZONE_X = .15
    DEADZONE_Y = .3


    gamefield = ObjectProperty(None)

    def __init__(self, **kwargs):
        src = f"{self.theme}/player.gif"
        super().__init__(source=src, **kwargs)

    def on_kv_post(self, base_widget):
        self.pos_x = self.ipos_x
        self.render()

        Clock.schedule_interval(self.run_physic, 1 / self.FPS)

    def on_factor(self, instance, value):
        self.size = (self.factor, self.factor)
        self.render()

    def on_ipos_x(self, instance, value):
        self.pos_x = self.ipos_x
        self.render()

    def on_ipos_y(self, instance, value):
        self.pos_y = self.ipos_y
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
                self.accel_y = -.5

            sx = self.speed_x + self.accel_x
            sy = self.speed_y + self.accel_y

            sx = max(-self.MAX_SPEED_X, min(self.MAX_SPEED_X, sx)) * self.SPEED_ATT_X
            sy = max(-self.MAX_SPEED_Y, min(self.MAX_SPEED_Y, sy)) * self.SPEED_ATT_X

            if abs(sx) < self.MIN_SPEED_X:
                sx = 0

            if abs(sy) < self.MIN_SPEED_Y:
                sy = 0

            px = self.pos_x
            py = self.pos_y

            src_left_limit = px + self.DEADZONE_X
            src_right_limit = px + 1 - self.DEADZONE_X
            src_bottom_limit = py
            src_top_limit = py + 1 - self.DEADZONE_Y

            dst_left_limit = src_left_limit + sx
            dst_right_limit = src_right_limit + sx
            dst_bottom_limit = src_bottom_limit + sy
            dst_top_limit = src_top_limit + sy

            if self.gamefield and (lmap := self.gamefield.map):
                R_valid = True
                L_valid = True
                T_valid = True
                B_valid = True

                if dst_left_limit < 0:  # left limit, move the player at visual x=0
                    sx = -src_left_limit
                    L_valid = False
                elif dst_right_limit >= len(lmap[0]):
                    sx = len(lmap[0]) - src_right_limit
                    R_valid = False

                if dst_top_limit < 0:  # low limit, fall
                    T_valid = False
                elif dst_bottom_limit >= len(lmap):
                    B_valid = False

                if L_valid:
                    if T_valid:
                        block = lmap[int(dst_top_limit)][int(dst_left_limit)]
                        if self.gamefield.is_wall(block):
                            if int(dst_left_limit) != int(src_left_limit) or int(dst_top_limit) != int(src_top_limit):
                                if sx <= 0: sx = 0  # int(dst_left_limit) - dst_left_limit
                                if sy > 0: sy = 0  # dst_top_limit - int(dst_top_limit)

                    if B_valid:
                        block = lmap[int(dst_bottom_limit)][int(dst_left_limit)]
                        if self.gamefield.is_wall(block):
                            if int(dst_left_limit) != int(src_left_limit) or int(dst_bottom_limit) != int(src_bottom_limit):
                                if sx <= 0: sx = 0  # int(dst_left_limit) - dst_left_limit
                                if sy <= 0: sy = 0  # int(dst_bottom_limit) - dst_bottom_limit

                if R_valid:
                    if T_valid:
                        block = lmap[int(dst_top_limit)][int(dst_right_limit)]
                        if self.gamefield.is_wall(block):
                            if int(dst_right_limit) != int(src_right_limit) or int(dst_top_limit) != int(src_top_limit):
                                if sx > 0:  sx = 0  # dst_right_limit - int(dst_right_limit)
                                if sy > 0: sy = 0  # sy = dst_top_limit - int(dst_top_limit)

                    if B_valid:
                        block = lmap[int(dst_bottom_limit)][int(dst_right_limit)]
                        if self.gamefield.is_wall(block):
                            if int(dst_right_limit) != int(src_right_limit) or int(dst_bottom_limit) != int(src_bottom_limit):
                                if sx > 0: sx = 0  # dst_right_limit - int(dst_right_limit)
                                if sy <= 0: sy = 0  # int(dst_bottom_limit) - dst_bottom_limit

            self.speed_x = sx
            self.speed_y = sy

            self.pos_x += sx
            self.pos_y += sy

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

