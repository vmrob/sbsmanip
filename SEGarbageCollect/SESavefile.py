import xml.etree.ElementTree as ET


class SESavefile:

    def __init__(self, filename):
        self._tree = ET.parse(filename)
        self._root = self._tree.getroot()

    def total_objects(self):
    	return len(self._root.find('SectorObjects').findall('MyObjectBuilder_EntityBase'));
