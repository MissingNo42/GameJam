import json

import kivy.resources
from kivy.animation import Animation

from core.ui.tile import Tile
from kivy.properties import NumericProperty, BooleanProperty, ListProperty, BoundedNumericProperty
from kivy.uix.effectwidget import ScanlinesEffect
from kivy.clock import Clock

from .player import Player
from .shaders import ChromaticAberationSickness1, ChromaticAberationSickness2, ChromaticAberationSickness0, \
    ChromaticAberationSickness3
from .theme import Theme
from .progressbar import BeerProgressBar

__all__ = (
    "GameField",
)


class GameField(Theme):
    FPS = 30

    move_right = BooleanProperty(False)
    move_left = BooleanProperty(False)
    jump = BooleanProperty(False)

    offsetX = NumericProperty(0)
    tile_size = NumericProperty(160)
    effects = ListProperty([])
    level = NumericProperty(0)
    map = ListProperty([])

    tick = 0

    life = BoundedNumericProperty(50, min=0, max=100, errorhandler=lambda x: 100 if x > 100 else 0)

    __slots__ = ("bg_00", "bg_01", "bg_02", "bg_03", "bg_04", "player", "progressbar")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg_00 = None
        self.bg_01 = None
        self.bg_02 = None
        self.bg_03 = None
        self.bg_04 = None
        self.player = None
        self.progressbar = None

        self.effects = []

    def on_size(self, instance, value):
        self.bg_00.size = (self.width * 4, self.height)
        self.bg_01.size = (self.width * 4, self.height)
        self.bg_02.size = (self.width * 4, self.height)
        self.bg_03.size = (self.width * 4, self.height)
        self.bg_04.size = (self.width * 4, self.height)
        self.player.ipos_x = self.width * 0.2 / self.tile_size
        self.progressbar.top = self.height * 0.9
        self.progressbar.width = self.width / 6
        self.progressbar.height = self.height / 10

    def on_kv_post(self, base_widget):
        self.bg_00 = Tile(source="bg_00.png", paralax=0.0, size=(self.width * 4, self.height))
        self.bg_01 = Tile(source="bg_01.png", paralax=0.2, size=(self.width * 4, self.height))
        self.bg_02 = Tile(source="bg_02.png", paralax=0.4, size=(self.width * 4, self.height))
        self.bg_03 = Tile(source="bg_03.png", paralax=0.6, size=(self.width * 4, self.height))
        self.bg_04 = Tile(source="bg_04.png", paralax=0.8, size=(self.width * 4, self.height))

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

        self.progressbar = BeerProgressBar(value=self.life,
                                           x=0,
                                           top=self.height * 0.8,
                                           height=self.height / 10,
                                           theme=self.theme)

        self.bind(life=self.progressbar.setter("value"))

        self.level = 1
        Clock.schedule_interval(self.update, 1 / self.FPS)

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
        self.add_widget(self.bg_04)
        self.add_widget(self.player)
        self.add_widget(self.progressbar)

        if self.map:
            for y, row in enumerate(self.map):
                for x, tile in enumerate(row):
                    if not tile:
                        continue
                    self.add_widget(Tile(source=f"block_{tile:02}.gif",
                                         y=y * self.tile_size,
                                         pos_x=x * self.tile_size,
                                         offsetX=self.offsetX,
                                         size=(self.tile_size, self.tile_size)))

    def on_offsetX(self, instance, value):
        for child in self.children:
            child.offsetX = value

    def clear_block(self, x : int, y : int):
        self.map[y][x] = 0
        self.render()

    def get_block(self, x : int, y : int) -> int:
        return self.map[y][x]

    def is_wall(self, block: int) -> bool:
        return block == 1

    """
    02 = germany
    03 = russia
    04 = ireland

    05 = banana
    """
    theme_name = ["germany", "russia", "ireland"]
    def trigger_block(self, x : int, y : int):
        b = self.get_block(x, y)
        if b >= 2 and b <= 4:
            self.theme = self.theme_name[b-2]
            self.clear_block(x, y)
            self.life += 25
        if b == 5:
            self.player.set_state("chute")



    def grid_size_x(self) -> int:
        return len(self.map[0])

    def grid_size_y(self) -> int:
        return len(self.map)

    def on_life(self, instance, value):
        if value <= 0:
            if self.player.physic_running:
                self.player.physic_running = False

                a = Animation(opacity=0, duration=1, transition="in_out_cubic")
                p = Animation(center_x=self.center_x, center_y=self.center_y, duration=2, transition="in_out_cubic")
                p.bind(on_complete=lambda *x: self.player.set_state("die"))
                for i in self.children:
                    if isinstance(i, Player):
                        p.start(i)
                    else:
                        a.start(i)
                self.effects = [ChromaticAberationSickness0()]
            return

        if value < 10:
            self.effects = [ChromaticAberationSickness0()]

        elif value < 30:
            self.effects = [ChromaticAberationSickness1()]

        elif value < 70:
            self.effects = [ChromaticAberationSickness2()]

        else:
            self.effects = [ChromaticAberationSickness3()]


    def update(self, dt):
        self.tick += 1
        self.player.update(dt)
        self.life -= 0.15

