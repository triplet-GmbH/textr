import os
from itertools import islice

from wcwidth import wcswidth  # type: ignore
from colorama.ansi import Fore


def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def bordered(text: str, pos: int, border: str, width: int = 40) -> str:
    """ Draws a bordered line of text
    
    >>> bordered("Foo", 3, "{-})
    <<< "{--Foo-----}"
    """
    assert len(border) == 3

    left, middle, right = list(border)
    base = left + width * middle + right
   
    return base[0:pos] + text + base[pos + wcswidth(text):]


def colorizer(color):
    def colorize(text):
        return color + text + Fore.RESET
    return colorize


def chunkify(it, size):
    it = iter(it)
    while True:
        chunk = list(islice(it, size))
        if chunk:
            yield chunk
        else:
            return
