from kivy.properties import NumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.progressbar import ProgressBar
from kivy.uix.widget import Widget
from .theme import Theme
from .tile import Tile


__all__ = (
    "BeerProgressBar",
)


class BeerProgressBar(Tile):
    value = NumericProperty(0)

    __slots__ = ("bar",)

    def __init__(self, **kwargs):
        self.bar = []
        super().__init__(source="beer.gif", **kwargs)

    def on_kv_post(self, base_widget):
        self.bar = [ProgressBar(value=self.value, max=100,
                               x=self.width / 2,
                               y=self.center_y + n * 3,
                               width=400,
                               height=50,
                               ) for n in range(-3, 4, 1)]

        for i in self.bar:
            self.add_widget(i)

    def on_offsetX(self, instance, value):
        pass

    def on_size(self, instance, value):
        super().on_size(instance, value)
        for n, bar in enumerate(self.bar):
            bar.x = 50 + self.width / 2
            bar.y = self.center_y + (n-3) * 3

    def on_pos(self, instance, value):
        for n, bar in enumerate(self.bar):
            bar.x = 50 + self.width / 2
            bar.y = self.center_y + (n-3) * 3

    def on_value(self, instance, value):
        for bar in self.bar:
            bar.value = value
