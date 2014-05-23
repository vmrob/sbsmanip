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
                                 help='scale world by the provided scalar')
        self.parser.add_argument('--remove-far',
                                 dest='distance',
                                 help='remove entities farther than the '
                                      'provided distance')
        self.parser.add_argument('--remove-debris',
                                 dest='debris_size',
                                 help='remove CubeGrid entities with less '
                                      'than DEBRIS_SIZE components')
        self.parser.add_argument('--remove-all',
                                 dest='remove_all',
                                 help='remove all entities from the game '
                                 'world, used best with white-list flags',
                                 action='store_true')
        self.parser.add_argument('--remove-pure-armor',
                                 dest='remove_armored',
                                 help='remove ships that are made of only armor',
                                 action='store_true')
        self.parser.set_defaults(whitelist_beacons=True)
        self.parser.add_argument('--whitelist',
                                 dest='whitelist',
                                 help='whitelist entities matching criteria. '
                                 'Valid options are beacons, players, '
                                 'asteroids. To use multiple criteria,'
                                 'separate them with a pipe symbol. Example: '
                                 '--whitelist beacons|players|asteroids')
        self.parser.add_argument('--remove-ship',
                                 dest='target_ship',
                                 help='remove instances of a specific ship. '
                                 'TARGET_SHIP is the path to a valid .sbc '
                                 'file')
        self.parser.add_argument('--scale-weld',
                                 dest='build_time_scalar',
                                 help='adjust the build time by a global '
                                 'scalar')
        self.parser.add_argument('--scale-disassembly',
                                 dest='disassembly_scalar',
                                 help='adjust the diassembly ratio by a '
                                 'global scalar')

    def parse(self):
        return self.parser.parse_args()

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
        for q in ('Armor', 'Reactor', 'Thrust', 'Cargo',
                  'Conveyor', 'Cockpit', 'Window', None):
            Stats._print_dict(block_dist, q)

    def print_station_stats(self):
        pass

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

    def __init__(self, options):
        self._parse_opts(options)

    def _parse_opts(self, options):
        self._opts = options.parse()
        self.filename = self._opts.filename

    def run(self):
        if (self._opts.build_time_scalar is not None or
                self._opts.disassembly_scalar is not None):
            self._run_cubeblocks_manip()
        else:
            self._run_savefile_manip()

    def _run_cubeblocks_manip(self):
        self.savefile = sbsmanip.io.CubeBlocksSBC(self.filename)

        changed = set()

        if self._opts.build_time_scalar is not None:
            mod = sbsmanip.modifier.ScaleAssemblyTime(
                self.savefile.definitions,
                self._opts.build_time_scalar)
            prepared = mod.prepare()
            changed |= set(prepared)
            mod.execute(prepared)

        if self._opts.disassembly_scalar is not None:
            mod = sbsmanip.modifier.ScaleDisassemblyTime(
                self.savefile.definitions,
                self._opts.disassembly_scalar)
            prepared = mod.prepare()
            changed |= set(prepared)
            mod.execute(prepared)

        if changed:
            print 'writing changes for %d %s' % (
                len(changed),
                'definition' if len(changed) == 1 else 'definitions')
            self.savefile.write(self.filename)
        else:
            print 'no applicable definitions'

    def _run_savefile_manip(self):
        self.savefile = sbsmanip.io.SBSFile(self.filename)

        self._print_stats()

        total_changed = []

        whitelist = self._get_whitelist()

        for e in whitelist:
            if type(e) == sbsmanip.sector.CubeGridEntity:
                print ('ignoring %20s due to powered beacon on board: %s'
                       % (e.id, ', '.join(e.beacon_names())))
            else:
                print 'ignoring %20s' % e.id

        if self._opts.remove_all:
            self._exec_mod(
                sbsmanip.modifier.RemoveAll(
                    self.savefile.sector),
                total_changed,
                'remove %d %s? [y/n] ',
                whitelist)

        if self._opts.remove_armored:
            self._exec_mod(
                sbsmanip.modifier.RemovePure(
                    self.savefile.sector,
                    ['LargeBlockArmorBlock', 
                     'LargeBlockArmorCorner', 
                     'LargeBlockArmorCornerInv', 
                     'LargeBlockArmorSlope', 
                     'LargeHeavyBlockArmorBlock', 
                     'LargeHeavyBlockArmorCorner', 
                     'LargeHeavyBlockArmorCornerInv', 
                     'LargeHeavyBlockArmorSlope', 
                     'SmallBlockArmorBlock', 
                     'SmallBlockArmorCorner', 
                     'SmallBlockArmorCornerInv', 
                     'SmallBlockArmorSlope', 
                     'SmallHeavyBlockArmorBlock', 
                     'SmallHeavyBlockArmorCorner', 
                     'SmallHeavyBlockArmorCornerInv', 
                     'SmallHeavyBlockArmorSlope']),
                total_changed,
                'remove %d %s? [y/n] ',
                whitelist)

        if self._opts.scale is not None:
            self._exec_mod(
                sbsmanip.modifier.Scale(
                    self.savefile.sector, float(self._opts.scale)),
                total_changed,
                'scale the positions of %d %s'
                ' by a factor of ' + self._opts.scale + '? [y/n] ')

        if self._opts.distance is not None:
            self._exec_mod(
                sbsmanip.modifier.RemoveFar(
                    self.savefile.sector, float(self._opts.distance)),
                total_changed,
                'remove %d %s? [y/n] ',
                whitelist)

        if self._opts.debris_size is not None:
            self._exec_mod(
                sbsmanip.modifier.RemoveSize(
                    self.savefile.sector, 0, float(self._opts.debris_size)),
                total_changed,
                'remove %d %s? [y/n] ',
                whitelist)

        if self._opts.target_ship is not None:
            target_ship = sbsmanip.io.XMLFile(self._opts.target_ship)
            target = sbsmanip.sector.CubeGridEntity(target_ship.root)
            self._exec_mod(
                sbsmanip.modifier.RemoveShip(
                    self.savefile.sector, target),
                total_changed,
                'remove %d %s? [y/n] ',
                whitelist)

        if total_changed:
            print 'writing changes for %d %s' % (
                len(total_changed),
                'entity' if len(total_changed) == 1 else 'entities')
            self.savefile.write(self.filename)

    def _exec_mod(self, mod, total_changed, confirm_message, whitelist=[]):
        prepared = mod.prepare()
        whitelist_ids = [e.id for e in whitelist]
        prepared = [e for e in prepared if e.id not in whitelist_ids]
        if prepared:
            self._print_prepared(prepared)
            response = raw_input(confirm_message % (
                len(prepared),
                'entity' if len(prepared) == 1 else 'entities'))
            if response == 'y' or response == 'Y':
                total_changed.extend(prepared)
                mod.execute(prepared)
        else:
            print 'no applicable entities'

    def _print_prepared(self, prepared):
        for e in prepared:
            distance = math.sqrt(
                e.position.x**2 +
                e.position.y**2 +
                e.position.z**2) / 1000
            if isinstance(e, sbsmanip.sector.CubeGridEntity):
                beacons = e.beacons()
                if beacons:
                    print ('type:  %-18s  id:  %20s  distance: %8.2f km  '
                           'components:  %5d  beacons:  %s'
                           % (e.type_name(),
                              e.id,
                              distance,
                              e.block_count(),
                              ', '.join(e.beacon_names())))
                else:
                    print ('type:  %-18s  id:  %20s  distance: %8.2f km  '
                           'components:  %5d'
                           % (e.type_name(), e.id, distance, e.block_count()))
            else:
                print ('type:  %-18s  id:  %20s  distance: %8.2f km'
                       % (e.type_name(), e.id, distance))

    @staticmethod
    def _print_divider(width=__default_divider_width):
        print '=' * width

    def _get_whitelist(self):
        whitelist = []

        if not self._opts.whitelist:
            return whitelist

        params = self._opts.whitelist.split('|')

        if 'beacons' in params:
            whitelist.extend([e for e in self.savefile.sector.entities(
                sbsmanip.sector.CubeGridEntity) if
                e.power_sources() and e.beacons()])
        if 'asteroids' in params:
            whitelist.extend([e for e in self.savefile.sector.entities(
                sbsmanip.sector.VoxelMapEntity)])
        if 'players' in params:
            whitelist.extend([e for e in self.savefile.sector.entities(
                sbsmanip.sector.CharacterEntity)])

        return whitelist

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


def main():
    options = Options()
    app = App(options)
    app.run()

if __name__ == '__main__':
    sys.exit(main())