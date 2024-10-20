from kivy import Config

Config.set("graphics", "resizable", "1")
Config.set("graphics", "width", "1600")
Config.set("graphics", "height", "900")

from kivy.logger import Logger
Logger.setLevel("INFO")

from kivy.properties import StringProperty, NumericProperty, ObjectProperty, BooleanProperty
from kivy.core.window import Window
from kivymd.app import MDApp as App
from kivy.lang import Builder
from os.path import dirname


class GameApp(App):

    move_right = BooleanProperty(False)
    move_left = BooleanProperty(False)
    jump = BooleanProperty(False)

    @staticmethod
    def to_window(*_):
        return 0, 0  # avoid crash on Window move due to cls.Keyboard

    def open_settings(self):
        pass  # Disable Kivy Config Panel on F1 press

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.y = 0
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down, on_key_up=self._on_keyboard_up)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down, on_key_up=self._on_keyboard_up)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.move_left = True
        elif keycode[1] == 'right':
            self.move_right = True
        elif keycode[1] == 'up':
            self.jump = True
        return True

    def _on_keyboard_up(self, keyboard, keycode):
        if keycode[1] == 'left':
            self.move_left = False
        elif keycode[1] == 'right':
            self.move_right = False
        elif keycode[1] == 'up':
            self.jump = False
        return True

    def build(self):
        self.title = "Malivresse"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"
        Builder.load_file(dirname(__file__) + "/layout/components.kv", rulesonly=True)
        return Builder.load_file(dirname(__file__) + "/layout/app.kv")



