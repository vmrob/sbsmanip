import sys

from .options import Options
from .SESavefile import SESavefile


class SESavefileApp:

    def __init__(self, options, args):
        self._parse_opts(options, args)


    def _parse_opts(self, options, args):
        opts =  options.parse(args)
        self.filename = opts.filename
        self.savefile = SESavefile(self.filename)

        self.show_stats = opts.show_stats
        if self.show_stats:
            self._print_stats()

    def _print_stats(self):
        print 'there are %d objects in the sector' % self.savefile.total_objects()


def main(args):
    options = Options()
    app = SESavefileApp(options, args)
    

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
