import os
from pynput import keyboard

from src.game import Game
from src.cli import cli


if __name__ == '__main__':
    # weight, heigth = cli()
    game = Game(25, 25, hardocode_mode=True)
    game.run()