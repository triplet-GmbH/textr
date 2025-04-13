# Textr

## Foreword

Who needs fancy interfaces? Having fun the good, old, boring way.

## Installation

Use your favorite pacakge manager to install it, e.g.

    pip install textr

By itself, it's not really usable, since its a library.

## Usage

### Example Game: Find the Mimic

In this game, you're presented with two Chests. If you open the normal chest,
you get a treasure and win. If you open the mimic chest, you die and lose.


    class Chest(Asset):
        name = 'Chest'

        def actions(self, game):
            pass
    
    class Mimic(Asset):
        name = 'Chest
        
        def actions(self, game):
            pass

    game = Game()
    game.add_asset