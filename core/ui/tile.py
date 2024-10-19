from core.ui.theme import Theme
from kivy.graphics.texture import Texture
from kivy.properties import NumericProperty
from kivy.uix.image import Image


class Tile(Image, Theme):
    offsetX = NumericProperty(0)
    pos_x = NumericProperty(0)
    paralax = NumericProperty(1)

    def __init__(self, source: str, **kwargs):
        src = f"{self.theme}/{source}"
        super().__init__(source=src, **kwargs)

    def on_theme(self, instance, value):
        super().on_theme(instance, value)
        self.source = f"{self.theme}/{self.source.split('/', 1)[-1]}"

    def on_offsetX(self, instance, value):
        self.x = self.pos_x - value * self.paralax

        if self.paralax != 1:
            tratio = self.texture.width / self.texture.height
            limit = tratio * self.height

            if self.offsetX * self.paralax > limit:
                self.offsetX = self.offsetX % (limit / self.paralax)
            elif self.offsetX * self.paralax < 0:
                self.offsetX = self.offsetX % (limit / self.paralax)

    def on_pos_x(self, instance, value):
        self.x = value - self.offsetX * self.paralax

    def on_texture(self, instance, value):
        self.config_texture(False)

    def on_size(self, instance, value):
        self.config_texture()

    def config_texture(self, tex: bool = True):
        self.texture: Texture

        if not self.texture:
            return

        if self.paralax == 1:
            self.texture.min_filter = 'nearest'
            self.texture.mag_filter = 'nearest'
        else:
            self.fit_mode = "fill"
            self.texture.wrap = 'repeat'
            ratio = self.width / self.height
            tratio = self.texture.width / self.texture.height
            print(ratio, tratio, ratio / tratio)
            self.texture.uvsize = (ratio / tratio, -1)

            if tex:
                t = self.texture
                self.texture = None
                self.texture = t
