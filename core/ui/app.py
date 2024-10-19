from kivy import Config

Config.set("graphics", "resizable", "1")
Config.set("graphics", "width", "1920")
Config.set("graphics", "height", "1080")

from kivy.logger import Logger
Logger.setLevel("INFO")

from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.core.window import Window
from kivymd.app import MDApp as App
from kivy.lang import Builder
from os.path import dirname


class GameApp(App):

    #world = ObjectProperty(None, allownone=True)
    offsetX = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.offsetX -= 10
        elif keycode[1] == 'right':
            self.offsetX += 10
        elif keycode[1] == 'up':
            pass #self.player2.center_y += 10
        elif keycode[1] == 'down':
            pass #self.player2.center_y -= 10
        return True

    def build(self):
        self.title = "GameJam"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"
        Builder.load_file(dirname(__file__) + "/layout/components.kv", rulesonly=True)
        return Builder.load_file(dirname(__file__) + "/layout/app.kv")



