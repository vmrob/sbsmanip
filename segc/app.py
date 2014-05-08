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
        self._opts = options.parse(args)
        self.filename = self._opts.filename
        self.savefile = sbsmanip.io.SBSFile(self.filename)

    def run(self):
        if self._opts.show_stats:
            self._print_stats()

    def _print_stats(self):

        sector = self.savefile.sector

        total = sector.entity_count()
        voxelmaps = sector.entity_count(sbsmanip.sector.VoxelMapEntity)
        cubegrids = sector.entity_count(sbsmanip.sector.CubeGridEntity)
        floating = sector.entity_count(sbsmanip.sector.FloatingObjectEntity)

        print 'Sector Statistics'
        print '======================='
        print 'Total entities:   %4d' % total
        print 'Asteroids:        %4d' % voxelmaps
        print 'Ships/Stations:   %4d' % cubegrids
        print 'Floating Objects: %4d' % floating
        print '======================='


def main(args):
    options = Options()
    app = App(options, args)
    app.run()

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))