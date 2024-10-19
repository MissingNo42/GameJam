import kivy.resources as res
import os

res.resource_add_path(os.path.dirname(__file__) + "/assets")
del res, os


from .app import GameApp
from .game_field import GameField

__all__ = (
    "GameApp",
)
