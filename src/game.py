import os
import random
import time
from pynput import keyboard

from src.snake import SnakeHead
from src.snake import SnakeBody
from utils.messages_errors import GAME_OVER


class Game(object):
    CHAR_OF_BODY_FIELD = '█'
    CHAR_OF_EMPTY_FIELD = ' '
    CHAR_OF_FRUIT_FIELD = '*'

    def __init__(self, columns, rows):
        self.rows = rows
        self.columns = columns
        self.table = Game.generate_table(self.rows, self.columns)
        position_x, position_y = self.generate_snake()
        self.snake = SnakeHead(position_x, position_y, [])
        self.direction = (1, 0)
        self.fruit = False
        self.direction_name = 'right'
        self.points = 0
        
        # Position to put snake on table
        
        self.update_table(self.CHAR_OF_BODY_FIELD)

    @staticmethod
    def generate_table(rows, columns):        
        return list(([Game.CHAR_OF_EMPTY_FIELD] * columns for row in range(rows)))

    def print(self):
        print(f'Your Score: ({self.points})'.center((self.columns * 2) + 2))
        print(self.generate_line_vertical())
        for row in self.table:
            print('|', *row, '|')
        print(self.generate_line_vertical())

    def generate_snake(self):
        position_x = random.randint(0, self.rows - 1)
        position_y = random.randint(0, self.columns - 1)

        return position_x, position_y
    
    def generate_line_vertical(self):
        return '_' * ((self.columns * 2) + 2)

    def update_table(self, char):
        try:
            self.table[self.snake.position_y][self.snake.position_x] = char

            if len(self.snake.parts) > 0:
                self.update_position_parts(0, char)
        except IndexError as err:
            raise Exception()

    def update_position_parts(self, part, char):
        if part > len(self.snake.parts) - 1:
            return None

        self.table[self.snake.parts[part].position_y][self.snake.parts[part].position_x] = char
        self.update_position_parts(part + 1, char)
    
    def add_fruit(self, pos_x, pos_y):
        self.table[pos_x][pos_y] = self.CHAR_OF_FRUIT_FIELD
        self.fruit = True

    def add_new_part(self):
        pos_x, pos_y = self.get_position_by_direction()

        self.snake.parts.append(SnakeBody(pos_x, pos_y))
        self.points += 1
        self.fruit = False
    
    def get_position_by_direction(self):
        if self.direction_name == 'right':
            return (self.snake.position_x - 1, self.snake.position_y)
        if self.direction_name == 'left':
            return (self.snake.position_x + 1, self.snake.position_y)
        if self.direction_name == 'up':
            return (self.snake.position_x, self.snake.position_y - 1)
        if self.direction_name == 'down':
            return (self.snake.position_x, self.snake.position_y + 1)
    
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
        self.update_table(self.CHAR_OF_EMPTY_FIELD)
        self.update_positions(new_x, new_y)
        self.update_table(self.CHAR_OF_BODY_FIELD)

        if not self.fruit:
            self.generate_random_fruit()
    
    def change_direction(self, *directions):
        self.direction = directions

    def detect_object(self, pos_x, pos_y):
        _object = self.table[pos_y][pos_x]

        if _object == self.CHAR_OF_FRUIT_FIELD:
            self.add_new_part()
        elif _object == self.CHAR_OF_BODY_FIELD:
            raise Exception()

    def generate_random_fruit(self):
        pos_x, pos_y = self.generate_snake()

        if self.table[pos_x][pos_y] == self.CHAR_OF_EMPTY_FIELD:
           return self.add_fruit(pos_x, pos_y)
    
        self.generate_random_fruit()

    def verify_move(self, key):
        name = key.name

        if name == 'right' and self.direction_name != 'left':
            self.change_direction(1, 0)
            self.direction_name = 'right'
        if name == 'left' and self.direction_name != 'right':
            self.change_direction(-1, 0)
            self.direction_name = 'left'
        if name == 'up' and self.direction_name != 'down':
            self.change_direction(0, -1)
            self.direction_name = 'up'
        if name == 'down' and self.direction_name != 'up':
            self.change_direction(0, 1)
            self.direction_name = 'down'

    def main_loop(self):
        try:
            while True:
                time.sleep(.5)
                os.system('clear')

                move_x, move_y = self.direction
                
                self.move_snake(move_x, move_y)
                self.print()
        except Exception as _:
            print(GAME_OVER.format(points=self.points))
    
    def keyboard_loop(self):
        listener = keyboard.Listener(on_press=self.verify_move)
        listener.start()

    def run(self):
        self.keyboard_loop()
        self.main_loop()
