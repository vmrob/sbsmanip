import xml.etree.ElementTree as ET


class _SESchema:

    sector_root = 'SectorObjects'
    entity_base = 'MyObjectBuilder_EntityBase'


class _XMLFile:

    def __init__(self, filename):
        self._tree = ET.parse(filename)
        self._root = self._tree.getroot()


class SBSFile(_XMLFile):

    def entity_count(self):
        return len(self._root.find(
            _SESchema.sector_root).findall(_SESchema.entity_base))
