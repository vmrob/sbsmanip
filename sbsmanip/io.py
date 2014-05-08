import xml.etree.ElementTree as ET

import sector
import cubeblocks


class XMLFile(object):

    def __init__(self, filename):
        self._tree = ET.parse(filename)
        self.root = self._tree.getroot()

    def write(self, filename):
        self._tree.write(filename)


class SBSFile(XMLFile):

    def __init__(self, filename):
        super(SBSFile, self).__init__(filename)
        self.sector = sector.Sector(self.root)


class CubeBlocksSBC(XMLFile):

    def __init__(self, filename):
        super(CubeBlocksSBC, self).__init__(filename)
        self.definitions = [cubeblocks.Definition(d) for d in self.root.find(
            'Definitions').findall('Definition')]