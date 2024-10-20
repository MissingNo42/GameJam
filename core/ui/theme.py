from kivy.event import EventDispatcher
from kivy.properties import StringProperty
from kivy.uix.widget import Widget

__all__ = (
    "Theme",
)


class Theme(Widget):
    theme = StringProperty("irland")

    def on_theme(self, instance, value):
        super().on_theme(instance, value)

        for i in self.children:
            if isinstance(i, Theme):
                i.theme = value
