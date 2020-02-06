from colorama import Fore
from colorama import Style


class SnakeHead(object):
    CHARS_DIRECTIONS = {
        'right': '►',
        'left': '◄',
        'up': '▲',
        'down': '▼'
    }

    def __init__(self, direction, position_x, position_y, parts):
        self.direction = self.CHARS_DIRECTIONS[direction]
        self.position_x = position_x
        self.position_y = position_y
        self.parts = parts

    def change_positions(self, position_x, position_y):
        self.position_x = position_x
        self.position_y = position_y

    def change_direction(self, direction):
        self.direction = self.CHARS_DIRECTIONS[direction]

    def get_direction(self):
        return Fore.GREEN + self.direction + Style.RESET_ALL

class SnakeBody(object):
    def __init__(self, position_x, position_y):
        self.position_x = position_x
        self.position_y = position_y

    def change_positions(self, pos_x, pos_y):
        self.position_x = pos_x
        self.position_y = pos_y

