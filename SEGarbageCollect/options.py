from argparse import ArgumentParser

class Options:

    def __init__(self):
        self.parser = ArgumentParser()
        self.parser.add_argument('filename',
                                 help='Space Engineers savefile to process')
        self.parser.add_argument('--stats',
                                dest='show_stats',
                                help='provide statistics on the savefile',
                                action='store_true')
        self.parser.set_defaults(show_stats=False)

    def parse(self, args=None):
        return self.parser.parse_args(args)

    def print_usage(self):
        self.parser.print_help()