import sys
import math

import sbsmanip.io
import sbsmanip.modifier

from argparse import ArgumentParser


class Options(object):

    def __init__(self):
        self.parser = ArgumentParser()
        self.parser.add_argument('filename',
                                 help='Space Engineers savefile to process')
        self.parser.add_argument('--show-stats',
                                 dest='show_stats',
                                 help='provide statistics on the savefile')
        self.parser.add_argument('--scale',
                                 dest='scale',
                                 help='scales world by the provided scalar')
        self.parser.add_argument('--remove-far',
                                 dest='clip_distance',
                                 help='removes entities farther than the provided distance')
    def parse(self, args=None):
        return self.parser.parse_args(args)

    def print_usage(self):
        self.parser.print_help()


class Stats(object):

    def __init__(self, sector_node):
        self._sector_node = sector_node

    def print_basic_stats(self):

        sector = self._sector_node

        total = sector.entity_count()
        voxelmaps = sector.entity_count(sbsmanip.sector.VoxelMapEntity)
        cubegrids = sector.entity_count(sbsmanip.sector.CubeGridEntity)
        floating = sector.entity_count(sbsmanip.sector.FloatingObjectEntity)

        App._print_divider()
        print 'Sector Statistics'
        App._print_divider()
        print 'Total entities:   %4d' % total
        print 'Asteroids:        %4d' % voxelmaps
        print 'Ships/Stations:   %4d' % cubegrids
        print 'Floating Objects: %4d' % floating

    def print_sector_distribution(self):
        
        sector = self._sector_node
        block_dist = sector.block_distribution()

        App._print_divider()
        print 'Sector Block Distribution'
        for q in ('Armor', 'Reactor', 'Thrust', 'Cargo', 'Conveyor', 'Cockpit', 'Window', None):
            Stats._print_dict(block_dist, q)
   
    def print_station_stats(self):
        sector = self._sector_node

    def print_ship_stats(self):
        pass 

    @staticmethod
    def _print_dict(d, filter=None):
        filtered = {}
        if filter is not None:
            filtered = dict((k, v) for (k, v) in d.iteritems() if filter in k)
        else:
            filtered = dict((k, v) for (k, v) in d.iteritems())

        App._print_divider()
        total = 0
        for k in filtered:
            total += filtered[k]
        print '  %-32s total: %5d' % ((filter if filter else 'Misc'), total)
        App._print_divider()            
        
        for k in sorted(filtered):
            print '%-41s %5d' % (k, filtered[k])
            d.pop(k, None)


class App(object):

    __default_divider_width = 48

    def __init__(self, options, args):
        self._parse_opts(options, args)

    def _parse_opts(self, options, args):
        self._opts = options.parse(args)
        self.filename = self._opts.filename
        self.savefile = sbsmanip.io.SBSFile(self.filename)

    def run(self):
        self._print_stats()

        prepared = []
        if self._opts.scale is not None:
            mod = sbsmanip.modifier.Scale(self.savefile.sector, self._opts.scale)
            p = mod.prepare()
            self._print_prepared(p)
            response = raw_input('scale the positions of these %d '
                'objects by a factor of %d? [y/n] ' % (len(p), float(self._opts.scale)))
            if response == 'y' or response == 'Y':
                prepared.extend(p)
                mod.execute(p)

        if self._opts.clip_distance is not None:
            mod = sbsmanip.modifier.RemoveFar(self.savefile.sector, float(self._opts.clip_distance))
            p = mod.prepare()
            self._print_prepared(p)
            response = raw_input('remove these these %d objects? [y/n] ' % len(p))
            if response == 'y' or response == 'Y':
                prepared.extend(p)
                mod.execute(p)

        if len(prepared):
            print 'writing changes for %d entities' % len(prepared)
            self.savefile.write(self.filename)

    def _print_prepared(self, prepared):
        for e in prepared:
            distance = math.sqrt(e.position.x**2 + e.position.y**2 + e.position.z**2) / 1000
            if isinstance(e, sbsmanip.sector.CubeGridEntity):
                print 'type:  %-18s  id:  %20s  distance: %8.2f km  components:  %5d' % (e.type_name(), e.id, distance, e.block_count())
            else:
                print 'type:  %-18s  id:  %20s  distance: %8.2f km' % (e.type_name(), e.id, distance)

    @staticmethod
    def _print_divider(width=__default_divider_width):
        print '=' * width

    def _print_stats(self):

        stats = Stats(self.savefile.sector)

        if not self._opts.show_stats:
            return

        param = self._opts.show_stats.split('|')

        if 'all' in param:
            param = ('ship', 'station', 'sector')

        if param:
            stats.print_basic_stats()

        if 'ship' in param:
            stats.print_ship_stats()

        if 'station' in param:
            stats.print_station_stats()

        if 'sector' in param:
            stats.print_sector_distribution()


def main(args):
    options = Options()
    app = App(options, args)
    app.run()

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))