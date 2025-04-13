"""
This game is basically the mimic game, but with more "strategy"

You can now pick up an a Zapper that can zap the mimic.
You can also pick up Charges that charge the Zapper.
The Zapper can only be used when fully charged.

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
        yield 'Looks harmless'

    def actions(self, game):
        yield 'open', self._open

    def _open(self, game: Game):
        game.end('You opened the chest! It was a mimic! You Lost!')

    def query_zap_target(self, game, data):
        return [self, *data]


class Zapper(Asset):
    name = 'Zapper'
    category = 'Swag'
    
    def description(self, game):
        charge = game.query('total_charge', 0)
        
        yield 'A device from a mad scientist'
        yield 'It zaps things'
        yield f"{charge} / 3"

    def actions(self, game):
        charge = game.query('total_charge', 0)
        if charge >= 3:
            yield 'activate', self._activate

    def _activate(self, game: Game):
        game.log('You activated the zapper')
        for target in game.query('zap_target', []):
            game.log('A mimic was zapped!')
            game.remove_asset(target)


class Charge(Asset):
    name = 'Charge'
    category = 'Swag'
    
    def __init__(self):
        self.picked_up = False

    def description(self, game):
        yield 'A pulsating gem stone'
        if not self.picked_up:
            yield 'It lies on the ground'
        else:
            yield 'Its attached to your zapper'

    def actions(self, game):
        if not self.picked_up:
            yield 'pick up', self._pick_up

    def _pick_up(self, game: Game):
        game.log('You picked up the charge')
        self.picked_up = True

    def query_total_charge(self, game, data):
        return data + (self.picked_up * 1)


game = Game()
game.add_asset(Chest())
game.add_asset(Mimic())
game.add_asset(Mimic())
game.add_asset(Zapper())
game.add_asset(Charge())
game.add_asset(Charge())
game.add_asset(Charge())


if __name__ == '__main__':
    game.main()
