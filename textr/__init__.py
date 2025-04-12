import colorama

from .game import Game, Asset
from .render import colorizer


def initialize():
    try:
        import win_unicode_console  # type: ignore
        win_unicode_console.enable()
    except ImportError as exc:
        pass

    colorama.init()


initialize()


__all__ = [
    'Game',
    'Asset',
    'initialize',
    'colorizer',
]
