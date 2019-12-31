import os
from pynput import keyboard

from src.game import Game
from src.cli import cli


if __name__ == '__main__':
    weight, heigth = cli()
    game = Game(weight, heigth)
    game.run()