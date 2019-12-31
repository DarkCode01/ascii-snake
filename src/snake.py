class SnakeHead(object):
    def __init__(self, position_x, position_y, parts):
        self.position_x = position_x
        self.position_y = position_y
        self.parts = parts

    def change_positions(self, position_x, position_y):
        self.position_x = position_x
        self.position_y = position_y


class SnakeBody(object):
    def __init__(self, position_x, position_y):
        self.position_x = position_x
        self.position_y = position_y

    def change_positions(self, pos_x, pos_y):
        self.position_x = pos_x
        self.position_y = pos_y

