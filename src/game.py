import os
import time
import random

from colorama import Fore
from colorama import Back
from colorama import Style
from pynput import keyboard

from utils import banners
from src.snake import SnakeHead
from src.snake import SnakeBody


class Game(object):
    CHAR_OF_BODY_FIELD = Fore.GREEN + 'o' + Style.RESET_ALL
    CHAR_OF_EMPTY_FIELD = Fore.BLACK + ' ' + Style.RESET_ALL
    CHAR_OF_FRUIT_FIELD = Fore.YELLOW + '*' + Style.RESET_ALL
    CHAR_OF_WALL_FIELD = Fore.YELLOW + '█' + Style.RESET_ALL
    CHAR_OF_BONUS_FIELD = Fore.YELLOW + '@' + Style.RESET_ALL

    LIMIT_OF_BONUS = 100

    def __init__(self, rows, columns, speed=0.075, hardocode_mode=False):
        self.started = False
        self.rows = rows
        self.columns = columns
        self.hardocode_mode = hardocode_mode
        self.speed = speed
        self.table = Game.generate_table(self.rows, self.columns)
        position_x, position_y = self.generate_snake()
        self.direction = (1, 0)
        self.direction_name = 'right'
        self.snake = SnakeHead(self.direction_name, position_x, position_y, [])
        self.fruit = False
        self.points = 0
        self.bonus = 0
        self.bonus_time = False
        self.bar_of_bonus = []
        self.pause = False
        self.walls_active = False
        
        # Position to put snake on table
        self.update_table(self.CHAR_OF_BODY_FIELD)

    @staticmethod
    def generate_table(rows, columns):        
        return list(([Game.CHAR_OF_EMPTY_FIELD] * rows for row in range(columns)))

    def print_header(self):
        print(f'Your Score: ({self.points})'.center((self.rows * 2) + 2))
        print(f'Hardcode Mode: ({self.hardocode_mode})'.center((self.rows * 2) + 2))
        print('[@] => Bonus Fruit (random point (1, 10))[*] Normal Fruit One point'.center((self.rows * 2) + 2))
        print('(Esc) => Pause'.center((self.rows * 2) + 2))
        print()
        print(f'Score of bonus: [{"".join(self.bar_of_bonus)}] {(int((self.bonus / 100) * 100))}%'.center((self.rows * 2) + 2))
        print()

        if self.bonus >= self.LIMIT_OF_BONUS:
            print(f'Press [SPACE] to active bonus'.center((self.rows * 2) + 2))

    def print(self):
        self.print_header()

        print(self.generate_line_vertical())
        for row in self.table:
            print('|', *row, '|')
        print(self.generate_line_vertical())

    def generate_snake(self):
        position_x = random.randint(0, self.rows - 1)
        position_y = random.randint(0, self.columns - 1)

        return position_x, position_y
    
    def generate_line_vertical(self):
        return '_' * ((self.rows * 2) + 2)

    def update_table(self, char, clean=False):
        try:
            self.table[self.snake.position_y][self.snake.position_x] = char if clean else self.snake.get_direction()

            if len(self.snake.parts) > 0:
                self.update_position_parts(0, char)
        except IndexError as err:
            raise Exception()

    def update_position_parts(self, part, char):
        if part > len(self.snake.parts) - 1:
            return None

        self.table[self.snake.parts[part].position_y][self.snake.parts[part].position_x] = char
        self.update_position_parts(part + 1, char)
    
    def add_object(self, pos_x, pos_y, char):
        self.table[pos_y][pos_x] = char

    def add_point_and_bonus(self):
        self.points += 1
        self.fruit = False

        if not self.bonus_time and self.bonus < self.LIMIT_OF_BONUS:
            self.bonus += 1

        if self.bonus < self.LIMIT_OF_BONUS:
            self.bonus_time = False
            self.bar_of_bonus.append(self.CHAR_OF_WALL_FIELD)
    
    def decrement_bonus_time(self):
        try:
            self.bonus -= 1
            self.bar_of_bonus.pop()
        except IndexError as _:
            self.bonus_time = False

    def add_new_part(self):
        self.snake.parts.append(SnakeBody(self.snake.position_x, self.snake.position_y))
        self.add_point_and_bonus()

    def change_positions_parts(self, part, last_pos_x, last_pos_y):
        if part > len(self.snake.parts) - 1:
            return None

        last_pos_x_part = self.snake.parts[part].position_x
        last_pos_y_part = self.snake.parts[part].position_y

        self.snake.parts[part].change_positions(last_pos_x, last_pos_y)
        self.change_positions_parts(part + 1, last_pos_x_part, last_pos_y_part)

    def update_positions(self, pos_x, pos_y):
        old_x = self.snake.position_x
        old_y = self.snake.position_y

        self.snake.change_positions(pos_x, pos_y)

        if len(self.snake.parts) > 0:
            self.change_positions_parts(0, old_x, old_y)
    
    def calcultate_new_position(self, pos_x, pos_y):
        new_x = self.snake.position_x + pos_x
        new_y = self.snake.position_y + pos_y

        new_x = new_x % self.rows
        new_y = new_y % self.columns

        return new_x, new_y

    def move_snake(self, pos_x, pos_y):
        new_x, new_y = self.calcultate_new_position(pos_x, pos_y)

        self.detect_object(new_x, new_y)
        self.update_table(self.CHAR_OF_EMPTY_FIELD, clean=True)
        self.update_positions(new_x, new_y)
        self.update_table(self.CHAR_OF_BODY_FIELD)

        if self.bonus_time:
            self.generate_random_object(self.CHAR_OF_FRUIT_FIELD)
            self.decrement_bonus_time()
        elif not self.fruit:
            char = random.choice((self.CHAR_OF_FRUIT_FIELD, self.CHAR_OF_BONUS_FIELD))

            self.generate_random_object(char)
            self.fruit = True

        if self.walls_active or self.hardocode_mode and self.points != 0 and (self.points % 2) == 0:
            self.generate_random_object(self.CHAR_OF_WALL_FIELD)
            self.walls_active = True
        if self.points != 0 and (self.points % 2) != 0:
            self.walls_active = False
    
    def change_direction(self, *directions):
        self.direction = directions

    def detect_object(self, pos_x, pos_y):
        _object = self.table[pos_y][pos_x]

        if _object == self.CHAR_OF_FRUIT_FIELD:
            self.add_new_part()
        if _object == self.CHAR_OF_BONUS_FIELD:
            for new_part in range(0, random.randint(1, 10)):
                self.add_new_part()
        elif _object == self.CHAR_OF_BODY_FIELD:
            raise Exception()
        elif _object == self.CHAR_OF_WALL_FIELD:
            raise Exception()

    def generate_random_object(self, char):
        pos_x, pos_y = self.generate_snake()

        if self.table[pos_y][pos_x] == self.CHAR_OF_EMPTY_FIELD:
           return self.add_object(pos_x, pos_y, char)
    
        self.generate_random_object(char)

    def verify_move(self, key):
        name = key.name

        if name == 'enter' and not self.started:
            self.started = True
        elif name == 'space' and self.bonus >= self.LIMIT_OF_BONUS:
            self.bonus_time = not self.bonus_time
        elif name == 'right' and self.direction_name != 'left':
            self.change_direction(1, 0)
            self.direction_name = 'right'
        elif name == 'left' and self.direction_name != 'right':
            self.change_direction(-1, 0)
            self.direction_name = 'left'
        elif name == 'up' and self.direction_name != 'down':
            self.change_direction(0, -1)
            self.direction_name = 'up'
        elif name == 'down' and self.direction_name != 'up':
            self.change_direction(0, 1)
            self.direction_name = 'down'
        elif name == 'esc':
            self.pause = not self.pause

        # changhe direction of snake's head...
        self.snake.change_direction(self.direction_name)

    def main_loop(self):
        try:
            while True:
                time.sleep(self.speed)
                os.system('clear')

                if not self.pause and self.started:
                    move_x, move_y = self.direction
                    
                    self.move_snake(move_x, move_y)
                    self.print()
                elif self.pause:
                    print(Fore.GREEN + banners.PAUSE + Style.RESET_ALL)
                else:
                    print(Fore.GREEN + banners.START_GAME + Style.RESET_ALL)
        except Exception as _:
            print(Fore.RED + banners.GAME_OVER.format(points=self.points) + Style.RESET_ALL)

    def keyboard_loop(self):
        listener = keyboard.Listener(on_press=self.verify_move)
        listener.start()

    def run(self):
        self.keyboard_loop()
        self.main_loop()
