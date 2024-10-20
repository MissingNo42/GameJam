import json

import kivy.resources
from core.ui.tile import Tile
from kivy.properties import NumericProperty, BooleanProperty, ListProperty
from kivy.uix.effectwidget import ScanlinesEffect

from .player import Player
from .theme import Theme
from .progressbar import BeerProgressBar

__all__ = (
    "GameField",
)


class GameField(Theme):
    move_right = BooleanProperty(False)
    move_left = BooleanProperty(False)
    jump = BooleanProperty(False)

    offsetX = NumericProperty(0)
    tile_size = NumericProperty(192)
    effects = ListProperty([])
    level = NumericProperty(0)
    map = ListProperty([])

    __slots__ = ("bg_00", "bg_01", "bg_02", "bg_03", "player", "progressbar")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg_00 = None
        self.bg_01 = None
        self.bg_02 = None
        self.bg_03 = None
        self.player = None
        self.progressbar = None
        # self.effects = [ScanlinesEffect()]

    def on_size(self, instance, value):
        self.bg_00.size = (self.width * 4, self.height)
        self.bg_01.size = (self.width * 4, self.height)
        self.bg_02.size = (self.width * 4, self.height)
        self.bg_03.size = (self.width * 4, self.height)
        self.player.ipos_x = self.width * 0.2 / self.tile_size
        self.progressbar.top = self.height * 0.9
        self.progressbar.width = self.width / 6
        self.progressbar.height = self.height / 10

    def on_kv_post(self, base_widget):
        self.bg_00 = Tile(source="bg_00.png", paralax=0.0, size=(self.width * 4, self.height))
        self.bg_01 = Tile(source="bg_01.png", paralax=0.3, size=(self.width * 4, self.height))
        self.bg_02 = Tile(source="bg_02.png", paralax=0.6, size=(self.width * 4, self.height))
        self.bg_03 = Tile(source="bg_03.png", paralax=0.8, size=(self.width * 4, self.height))

        self.player = Player(gamefield=self,
                             factor=self.tile_size,
                             ipos_y=2,
                             ipos_x=self.width * 0.2 / self.tile_size,
                             move_right=self.move_right,
                             move_left=self.move_left,
                             jump=self.jump)

        self.bind(move_right=self.player.setter("move_right"))
        self.bind(move_left=self.player.setter("move_left"))
        self.bind(jump=self.player.setter("jump"))

        self.player.bind(pos_x=self.move)

        self.progressbar = BeerProgressBar(value=50,
                                           x=0,
                                           top=self.height * 0.8,
                                           height=self.height / 10,
                                           theme=self.theme)

        self.level = 1

    def on_level(self, instance, value):
        path = kivy.resources.resource_find(f"levels/level_{value:02}.json")
        with open(path, "r") as f:
            data = json.load(f)
            self.theme = data["theme"]
            self.map = list(reversed(data["map"]))

    def on_map(self, instance, value):
        self.render()

    def move(self, instance, value):
        self.offsetX = (value - instance.ipos_x) * self.tile_size

    def on_tile_size(self, instance, value):
        self.player.factor = value
        self.render()

    def render(self):
        self.clear_widgets()

        self.add_widget(self.bg_00)
        self.add_widget(self.bg_01)
        self.add_widget(self.bg_02)
        self.add_widget(self.bg_03)
        self.add_widget(self.player)
        self.add_widget(self.progressbar)

        if self.map:
            for y, row in enumerate(self.map):
                for x, tile in enumerate(row):
                    if not tile:
                        continue
                    self.add_widget(Tile(source=f"block_{tile:02}.png",
                                         y=y * self.tile_size,
                                         pos_x=x * self.tile_size,
                                         offsetX=self.offsetX,
                                         size=(self.tile_size, self.tile_size)))

    def on_offsetX(self, instance, value):
        for child in self.children:
            child.offsetX = value

    def get_block(self, x : int, y : int) -> Tile:
        return self.map[y][x]

    def is_wall(self, block: int) -> bool:
        return block != 0
    
    def trigger_block(self, x : int, y : int):
        pass

    def grid_size_x(self) -> int:
        return len(self.map[0])
    
    def grid_size_y(self) -> int:
        return len(self.map)
