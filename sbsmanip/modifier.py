import sector
import math


class Scale(object):

    def __init__(self, sector, scalar):
        self._sector = sector
        self._scalar = scalar

    def prepare(self):
        return [e for e in self._sector.entities()]

    def execute(self, prepared):
        for e in prepared:
            new_pos = sector.Vector3f(x=e.position.x * self._scalar,
                                      y=e.position.y * self._scalar,
                                      z=e.position.z * self._scalar)
            e.set_position(new_pos)


class RemoveFar(object):

    def __init__(self, sector, clip_distance):
        self._sector = sector
        self._clip_distance = clip_distance

    @staticmethod
    def _distance(pos):
        return math.sqrt(pos.x**2 + pos.y**2 + pos.z**2)

    def prepare(self):
        return [e for e in self._sector.entities()
                if self._distance(e.position) > self._clip_distance]

    def execute(self, prepared):
        self._sector.remove_entities(prepared)


class RemoveSize(object):

    def __init__(self, sector, lower_bound, upper_bound):
        self._sector = sector
        self._lower_bound = lower_bound
        self._upper_bound = upper_bound

    def prepare(self):
        return [e for e in self._sector.entities(sector.CubeGridEntity)
                if self._lower_bound < e.block_count() < self._upper_bound]

    def execute(self, prepared):
        self._sector.remove_entities(prepared)


class RemoveShip(object):

    def __init__(self, sector, target_entity):
        self._sector = sector
        self._target_block_distribution = target_entity.block_distribution()

    def prepare(self):
        return [e for e in self._sector.entities(sector.CubeGridEntity)
                if e.block_distribution() == self._target_block_distribution]

    def execute(self, prepared):
        self._sector.remove_entities(prepared)


class RemoveAll(object):

    def __init__(self, sector):
        self._sector = sector

    def prepare(self):
        return [e for e in self._sector.entities()]

    def execute(self, prepared):
        self._sector.remove_entities(prepared)


class RemovePure(object):

    def __init__(self, sector, whitelist):
        '''Will remove all ships that are made purely of the elements listed in the whitelist'''
        self._sector = sector
        self._whitelist = whitelist

    def prepare(self):
        entities = [e for e in self._sector.entities(sector.CubeGridEntity)]
        ret = []
        for e in entities:
            should_delete = True
            for k in e.block_distribution():
                if k not in self._whitelist:
                    should_delete = False
                    break
            if should_delete:
                ret.append(e)
        return ret

    def execute(self, prepared):
        self._sector.remove_entities(prepared)


class ScaleAssemblyTime(object):

    def __init__(self, definitions, scalar):
        self._definitions = definitions
        self._scalar = scalar

    def prepare(self):
        return [d for d in self._definitions]

    def execute(self, prepared):
        for d in prepared:
            d.build_time = d.build_time * float(self._scalar)


class ScaleDisassemblyTime(object):

    def __init__(self, definitions, scalar):
        self._definitions = definitions
        self._scalar = scalar

    def prepare(self):
        return [d for d in self._definitions]

    def execute(self, prepared):
        for d in prepared:
            d.disassembly_ratio = d.disassembly_ratio * float(self._scalar)