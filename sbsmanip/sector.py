import collections

Vector3f = collections.namedtuple('Vector3f', ['x', 'y', 'z'])


class Block(object):

    def __init__(self, block_node):
        self.block_node = block_node

    def subtype_name(self):
        subtype = self.block_node.find('SubtypeName')
        if subtype is not None and subtype.text is not None:
            return subtype.text

    def builder_name(self):
        name = self.block_node.get(
            '{http://www.w3.org/2001/XMLSchema-instance}type')
        if name:
            return name.replace('MyObjectBuilder_', '', 1)

    def custom_name(self):
        custom = self.block_node.find('CustomName')
        if custom is not None and custom.text is not None:
            return custom.text

    def id(self):
        id = self.block_node.find('EntityId')
        if id is not None and id.text is not None:
            return id

    def complete(self):
        return self.block_node.find('BuildPercent') is None

    def type_name(self):
        subtype = self.subtype_name()
        builder = self.builder_name()
        if builder is None:
            return subtype
        if subtype is None:
            return builder
        return builder + ':' + subtype


class _EntityBase(object):

    def __init__(self, entity_node):
        self.entity_node = entity_node

    @property
    def position(self):
        position_node = self.entity_node.find(
            'PositionAndOrientation').find('Position')

        x = float(position_node.get('x'))
        y = float(position_node.get('y'))
        z = float(position_node.get('z'))

        return Vector3f(x=x, y=y, z=z)

    def set_position(self, vec):
        position_node = self.entity_node.find(
            'PositionAndOrientation').find('Position')

        position_node.set('x', str(vec.x))
        position_node.set('y', str(vec.y))
        position_node.set('z', str(vec.z))

    @property
    def id(self):
        return self.entity_node.find('EntityId').text

    def type_name(self):
        name = self.entity_node.get(
            '{http://www.w3.org/2001/XMLSchema-instance}type')
        return name.replace('MyObjectBuilder_', '', 1)


class VoxelMapEntity(_EntityBase):
    pass


class FloatingObjectEntity(_EntityBase):
    pass


class CharacterEntity(_EntityBase):
    pass


class MeteorEntity(_EntityBase):
    pass


class CubeGridEntity(_EntityBase):

    def __init__(self, entity_node):
        super(CubeGridEntity, self).__init__(entity_node)
        self._blocks = self.entity_node.find(
            'CubeBlocks').findall('MyObjectBuilder_CubeBlock')
        self._static_node = self.entity_node.find('IsStatic')
        self._static = (self._static_node is not None
                        and self._static_node.text == 'true')

    def block_count(self):
        return len(self._blocks)

    def blocks(self):
        for block in self._blocks:
            yield Block(block)

    def block_distribution(self):
        d = collections.defaultdict(int)
        for block in self._blocks:
            name = Block(block).type_name()
            d[name] += 1
        return d

    def beacons(self):
        return [b for b in self.blocks()
                if "Beacon" in b.type_name() and b.complete()]

    def beacon_names(self):
        return [b.custom_name()
                if b.custom_name() else "unknown"
                for b in self.beacons()]

    def power_sources(self):
        sources = [b for b in self.blocks()
                   if "Reactor" in b.type_name() and b.complete()]
        sources.extend([b for b in self.blocks()
                        if "Solar" in b.type_name() and b.complete()])
        return sources

    @property
    def static(self):
        return self._static

    @static.setter
    def static(self, value):
        self._static_node.text = 'true' if value else 'false'
        self._static = value


def EntityFactory(entity_node):
    node = _EntityBase(entity_node)
    type_name = node.type_name()
    if type_name == 'CubeGrid':
        return CubeGridEntity(entity_node)
    elif type_name == 'VoxelMap':
        return VoxelMapEntity(entity_node)
    elif type_name == 'FloatingObject':
        return FloatingObjectEntity(entity_node)
    elif type_name == 'Character':
        return CharacterEntity(entity_node)
    elif type_name == 'Meteor':
        return MeteorEntity(entity_node)
    print '%s is an invalid type_name' % type_name
    raise


class Sector(object):

    def __init__(self, sector_root_node):
        self._sector_root = sector_root_node
        self._sector_objects = self._sector_root.find('SectorObjects')

    def entity_count(self, entity_type=_EntityBase):
        count = 0
        for e in self.entities():
            if isinstance(e, entity_type):
                count += 1
        return count

    def entities(self, entity_type=_EntityBase):
        for entity in self._sector_objects.findall(
                'MyObjectBuilder_EntityBase'):
            e = EntityFactory(entity)
            if isinstance(e, entity_type):
                yield e

    def remove_entities(self, entities_list):
        for e in entities_list:
            self._sector_objects.remove(e.entity_node)

    def block_distribution(self):
        d = collections.defaultdict(int)
        for e in self.entities():
            if type(e) is CubeGridEntity:
                ed = e.block_distribution()
                for k in ed:
                    d[k] += ed[k]
        return d
