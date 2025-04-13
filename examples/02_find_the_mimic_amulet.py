"""
This game is basically the mimic game, but with more "strategy"

You can now pick up an Amulet that reveals the mimic.

"""
from textr import Asset, Game


class Chest(Asset):
    name = 'Chest'
    category = 'Treasure'

    def description(self, game):
        yield 'Looks harmless'

    def actions(self, game):
        yield 'open', self._open
    
    def _open(self, game: Game):
        game.end('You opened the chest! You found some gold! You Won!') 


class Mimic(Asset):
    name = 'Chest'
    category = 'Treasure'

    def description(self, game):
        if game.query('true_vision', False):
            yield 'Looks like a mimic'
        else:
            yield 'Looks harmless'

    def actions(self, game):
        yield 'open', self._open

    def _open(self, game: Game):
        game.end('You opened the chest! It was a mimic! You Lost!')


class Amulet(Asset):
    name = 'Amulet'
    category = 'Swag'
    
    def __init__(self):
        self.worn = False

    def description(self, game):
        if not self.worn:
            yield 'A nice amulet, lying on the ground'
        else:
            yield 'A nice amulet, worn by you'

    def actions(self, game):
        if not self.worn:
            yield 'pick up', self._pick_up
        else:
            yield 'take off', self._take_off

    def _pick_up(self, game: Game):
        game.log('You picked up the amulet')
        self.worn = True

    def _take_off(self, game: Game):
        game.log('You took off the amulet')
        self.worn = False
    
    def query_true_vision(self, game, data):
        return self.worn


game = Game()
game.add_asset(Chest())
game.add_asset(Mimic())
game.add_asset(Mimic())
game.add_asset(Amulet())


if __name__ == '__main__':
    game.main()
