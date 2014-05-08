import xml.etree.ElementTree as ET

import sector


class _XMLFile(object):

    def __init__(self, filename):
        self._tree = ET.parse(filename)
        self._root = self._tree.getroot()

    def write(self, filename):
        self._tree.write(filename)


class SBSFile(_XMLFile):

    def __init__(self, filename):
        super(SBSFile, self).__init__(filename)
        self.sector = sector.Sector(self._root)