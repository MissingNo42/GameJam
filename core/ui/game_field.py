from kivy.graphics.texture import Texture
from kivy.properties import NumericProperty, BooleanProperty, ListProperty
from kivy.uix.image import Image

from .player import Player
from .theme import Theme

__all__ = (
    "GameField",
    "Tile",
)


class Tile(Image, Theme):
    offsetX = NumericProperty(0)
    pos_x = NumericProperty(0)
    paralax = NumericProperty(1)

    def __init__(self, source: str, **kwargs):
        src = f"{self.theme}/{source}"
        super().__init__(source=src, **kwargs)

    def on_theme(self, instance, value):
        super().on_theme(instance, value)
        self.source = f"{self.theme}/{self.source}"

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

    def on_pixel(self, instance, value):
        self.config_texture()

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
            self.texture.uvsize = (ratio / tratio, -1)

            if tex:
                t = self.texture
                self.texture = None
                self.texture = t


class GameField(Theme):
    move_right = BooleanProperty(False)
    move_left = BooleanProperty(False)
    jump = BooleanProperty(False)

    offsetX = NumericProperty(0)
    tile_size = NumericProperty(256)
    effects = ListProperty([])

    __slots__ = ("bg_00", "bg_01", "bg_02", "player")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg_00 = None
        self.bg_01 = None
        self.bg_02 = None
        self.player = None

    def on_size(self, instance, value):
        self.bg_00.size = (self.width * 2, self.height)
        self.bg_01.size = (self.width * 2, self.height)
        self.bg_02.size = (self.width * 2, self.height)

    def on_kv_post(self, base_widget):
        self.bg_00 = Tile(source="bg_00.png", paralax=0.0, size=(self.width * 2, self.height))
        self.bg_01 = Tile(source="bg_01.png", paralax=0.3, size=(self.width * 2, self.height))
        self.bg_02 = Tile(source="bg_02.png", paralax=0.6, size=(self.width * 2, self.height))

        self.player = Player(factor=self.tile_size,
                             pos_y=2,
                             pos_x=self.width * 0.2 / self.tile_size,
                             move_right=self.move_right,
                             move_left=self.move_left,
                             jump=self.jump)

        self.bind(move_right=self.player.setter("move_right"))
        self.bind(move_left=self.player.setter("move_left"))
        self.bind(jump=self.player.setter("jump"))

        self.player.bind(pos_x=self.move)

        self.load_level()

    def move(self, instance, value):
        self.offsetX = (value - instance.ipos_x) * self.tile_size

    def on_tile_size(self, instance, value):
        self.player.factor = value
        self.load_level()

    def load_level(self):
        self.clear_widgets()

        self.add_widget(self.bg_00)
        self.add_widget(self.bg_01)
        self.add_widget(self.bg_02)
        self.add_widget(self.player)

        return
        for x in range(0, 10):
            for y in range(0, 10):
                tile = Tile(source="player.gif",
                            y=y * self.tile_size,
                            pos_x=x * self.tile_size,
                            offsetX=self.offsetX,
                            size=(self.tile_size, self.tile_size))

                self.add_widget(tile)

    def on_offsetX(self, instance, value):
        for child in self.children:
            child.offsetX = value
