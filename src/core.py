from os import system

from src.table import Table


class Core(object):

    @staticmethod
    def run():
        while True:
            table = Table(5, 5)
            system('clear')

    @staticmethod
    def stop():
        pass