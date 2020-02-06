import colorama

from src.game import Game
from src.setup import setup


if __name__ == '__main__':
    colorama.init()
    config = setup()

    # get parameters config...
    hardcode_mode = config.get('hardcode_mode')
    dimensions = config.get('dimensions')

    game = Game(
        dimensions.get('columns'),
        dimensions.get('rows'),
        speed=0.10,
        hardocode_mode=False
    )
    game.run()
