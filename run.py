import os
from pynput import keyboard

from src.game import Game
from src.cli import cli


if __name__ == '__main__':
    hardocode_mode = cli()
    game = Game(25, 25, hardocode_mode=hardocode_mode)
    game.run()