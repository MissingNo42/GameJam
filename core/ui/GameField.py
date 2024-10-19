from kivy.properties import NumericProperty
from kivy.uix.effectwidget import EffectWidget, ScanlinesEffect
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.image import Image

class Tile(Image):
    offsetX = NumericProperty(0)
    pos_x = NumericProperty(0)

    def on_offsetX(self, instance, value):
        self.x = self.pos_x - value

    def on_pos_x(self, instance, value):
        self.x = value - self.offsetX

    def on_texture(self, instance, value):
        value.mag_filter = 'nearest'


class GameField(Widget):

    offsetX = NumericProperty(0)
    tile_size = NumericProperty(128)

    def on_kv_post(self, base_widget):
        self.load_level()

    def load_level(self):
        self.clear_widgets()

        ScanlinesEffect

        for x in range(0, 10):
            for y in range(0, 10):
                tile = Tile()
                if y == 0:
                    tile.source = "player.png"
                elif y < 5:
                    tile.source = "kirbo.png"
                else:
                    tile.source = "ph.png"
                tile.size = (self.tile_size, self.tile_size)
                tile.y = y * self.tile_size
                tile.pos_x = x * self.tile_size
                tile.offsetX = self.offsetX
                self.add_widget(tile)

    def on_offsetX(self, instance, value):
        for child in self.children:
            child.offsetX = value

