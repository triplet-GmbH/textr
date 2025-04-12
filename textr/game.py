from re import I
from typing import Any, Iterable, Callable
from itertools import chain, groupby, zip_longest
from functools import reduce

from pynput import keyboard
from pynput.keyboard import Key

from .render import clear_screen, bordered, chunkify


type AssetActionHandler = Callable[['Game'], None]
type PrintModifier = Callable[[str], str]


class Asset(object):
    name: str = 'Asset'
    category: str = 'Game'
    order: int = 0

    def actions(self, game: 'Game') -> Iterable[tuple[str, AssetActionHandler]]:
        """ A list of actions this asset offers the player

        :returns:
            An Iterable of (name, handler). The Action is presented on the
            asset, if the player selects it, the handler will be called
        """
        return []

    def description(self, game: 'Game') -> Iterable[str]:
        """ The description of this asset.

        :returns:
            The lines of text that will be displayed on the asset.
        """
        return []

    def visible(self, game: 'Game') -> bool:
        """ The visibility of this asset.

        :returns:
            A boolean indicating if this asset should be displayed.
        """
        return True

    def _query[T](self, game: 'Game', type: str, data: T) -> T:
        handler = getattr(self,
                            'query_{}'.format(type),
                            lambda game, data: data)
        return handler(game, data)

    def _trigger_event(self, game: 'Game', type: str, data: Any):
        handler = getattr(self, 'on_{}'.format(type), None)
        if handler:
            return handler(game, data)


class Game(object):

    print_modifier: list[PrintModifier]
    assets: list[Asset]
    categories: list[str]
    over: str | None

    def __init__(self, categories: list[str] = []):
        self.print_modifier = []
        self.assets = []
        self.categories = categories
        self.over = None

    def register_print_modifiers(self, *modifiers: PrintModifier):
        """ Adds a print modifier to the game.

        The print modifier is a function that will be called on every line
        printed to the screen. It can be used to add color or other effects.

        :param func:
            A function that takes the string to be printed and returns a modified
            string.
        """
        self.print_modifier.extend(modifiers)

    def add_asset[T: Asset](self, asset: T) -> T:
        """ Adds an asset to the game.

        The asset will now reveive events and queries and can be displayed in
        the game.
        
        :param asset:
            The asset to add.
        :returns:
            The asset that was added.
        """
        self.assets.append(asset)
        return asset

    def remove_asset(self, asset: Asset):
        """ Removes an asset from the game.
        
        The asset will no longer receive events and queries and will not be
        displayed in the game anymore.

        :param asset:
            The asset to remove.
        """
        self.assets.remove(asset)

    def trigger_event(self, type: str, data: Any):
        """ Triggers an event on all assets

        Calls all `on_{type}` methods of all assets with the given data.
        
        Example:

            class Flower(Asset):
                name = 'Flower'

                def __init__(self, size):
                    self.size = size

                def on_grow(self, game: Game, data: int):
                    self.size += data

            game = Game()
            tulip = game.add_asset(Flower(size=1))
            rose = game.add_asset(Flower(size=2))

            game.trigger_event('grow', 1)
            assert tulip.size == 2
            assert rose.size == 3

        :param type:
            The type of event to trigger.
        """
        for asset in self.assets:
            asset._trigger_event(self, type, data)

    def query[T](self, type: str, data: T) -> T:
        """ Queries all assets

        Applies all `query_{type}` methods of all assets to `data`.
        This is similar to a `reduce` functionality.

        Example:

            class Chest(Asset):
                name = 'Chest'

                def __init__(self, gold_content):
                    self.gold_content = gold_content

                def query_total_loot(self, game: Game, data: int) -> int:
                    return data + self.gold_content

            game = Game()
            game.add_asset(Chest(gold_content=100))
            game.add_asset(Chest(gold_content=50))

            total_loot = game.query('total_loot', 0)
            assert total_loot == 150

        :param type:
            The type of query to perform.

            E.g. if type is `"xxx"`, the method `query_xxx` will be called on
            all assets that have it.

        :param data:
            The initial data to pass to the query.
        """
        for asset in self.assets:
            data = asset._query(self, type, data)
        return data

    def end(self, reason: str):
        """ Ends the game.

        Leads to a game over screen with `reason` as the message.

        :param reason:
            The reason for the game over, that is displayed to the player.
            E.g. "You died" or "You won".
        """
        self.over = reason

    def log(self, text: str):
        """ Informs the player about something.

        :param text:
            The text to display, e.g. "You found a treasure chest".
        """
        self._print(text)

    def asset_categories(self) -> Iterable[tuple[str, Iterable[Asset]]]:
        """ Groups the assets by their category."""
        def order(a: Asset) -> tuple[int, int]:
            return ((self.categories.index(a.category), a.order)
                        if a.category in self.categories
                        else (999, a.order))

        def group(a: Asset) -> str:
            return a.category

        visible_assets = (a for a in self.assets if a.visible(self))

        return groupby(sorted(visible_assets, key=order), key=group)

    def render_asset(self, asset: Asset, focus: int) -> Iterable[str]:
        desc = list(asset.description(self))
        actions = list(asset.actions(self))

        yield bordered(' ' + asset.name + ' ', 3, '┌─┐')

        for line in desc:
            yield bordered(line, 2, '│ │')

        if desc and actions:
            yield bordered('', 0, '│ │')

        for index, (title, _) in enumerate(actions):
            option = '{} {}'.format('=>' if index == focus else '->', title)
            yield bordered(option, 2, '│ │')

        yield bordered('', 0, '└─┘')

    def main(self):
        clear_screen()

        focus = 0

        while self.over is None:
            offset = 0
            all_actions = []

            for category, assets in self.asset_categories():

                self._print('')
                self._print(bordered(' ' + category + ' ', 3, '==='))
                self._print('')

                for row in chunkify(assets, 3):
                    actions = [list(asset.actions(self)) for asset in row]
                    offsets = [sum(len(a) for a in actions[0:i]) for i in range(len(actions))]

                    lines = [self.render_asset(asset, focus - offset - o)
                                    for asset, o
                                    in zip(row, offsets)]

                    for l in zip_longest(*lines):
                        self._print(''.join(line or ' ' * 42 for line in l))

                    all_actions.extend(chain(*actions))
                    offset += sum((len(a) for a in actions), 0)

            nav = get_navigation()

            clear_screen()

            if nav == 'up':
                focus = max(focus - 1, 0)
            elif nav == 'down':
                focus = min(focus + 1, len(all_actions) - 1)
            elif nav == 'enter':
                _, func = all_actions[focus]
                func(self)

            self._print('')

        clear_screen()

        self._print(self.over)

    def _print(self, text):
        """ Prints text to the screen.
        
        Applies all print modifiers to the text before printing 
        """
        print(reduce(lambda t, f: f(t), self.print_modifier, text))


def get_navigation():
    class KeyPressedEvent(Exception):
        def __init__(self, key):
            self.key = key

    def on_press(key):
        if key == Key.down:
            raise KeyPressedEvent('down')
        elif key == Key.up:
            raise KeyPressedEvent('up')
        elif key == Key.enter:
            raise KeyPressedEvent('enter')

    with keyboard.Listener(on_press=on_press) as listener:
        try:
            listener.join()
        except KeyPressedEvent as evt:
            return evt.key
