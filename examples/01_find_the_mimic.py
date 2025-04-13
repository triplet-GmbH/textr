"""
In this game, you're presented with two Chests.

If you open the normal chest, you get a treasure and win. (The Good Ending)
If you open the mimic chest, you die and lose. (The Bad Ending)

"""
from textr import Asset, Game


class Chest(Asset):
    name = 'Chest'

    def description(self, game):
        yield 'Looks harmless'

    def actions(self, game):
        yield 'open', self._open
    
    def _open(self, game: Game):
        game.end('You opened the chest! You found some gold! You Won!') 


class Mimic(Asset):
    name = 'Chest'

    def description(self, game):
        yield 'Looks harmless'

    def actions(self, game):
        yield 'open', self._open

    def _open(self, game: Game):
        game.end('You opened the chest! It was a mimic! You Lost!')


game = Game()
game.add_asset(Chest())
game.add_asset(Mimic())
game.add_asset(Mimic())


if __name__ == '__main__':
    game.main()
