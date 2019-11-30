import argparse


class Arguments(object):
    def __init__(self):
        self.__parser = argparse.ArgumentParser(description = 'Script to run MLaaS')
        self.add_arguments()

    def add_arguments(self):
        self.__parser.add_argument(
            '-f', '--file',
            action = 'store',
            required = False
        )
        self.__parser.add_argument(
            '-c', '--class',
            action = 'store',
            required = False
            )
        self.__parser.add_argument(
            '-s', '--sep',
            action = 'store',
            required = False,
            default = ';'
        )
        self.__parser.add_argument(
            '-e', '--encoding',
            action = 'store',
            required = False,
            default = 'latin-1'
        )

    @property
    def parser(self):
        return self.__parser
