import sys
import sbsmanip.io

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


class App:

    def __init__(self, options, args):
        self._parse_opts(options, args)

    def _parse_opts(self, options, args):
        opts = options.parse(args)
        self.filename = opts.filename
        self.savefile = sbsmanip.io.SBSFile(self.filename)

        self.show_stats = opts.show_stats
        if self.show_stats:
            self._print_stats()

    def _print_stats(self):
        print ('there are %d entities in the sector'
               % self.savefile.entity_count())


def main(args):
    options = Options()
    app = App(options, args)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))