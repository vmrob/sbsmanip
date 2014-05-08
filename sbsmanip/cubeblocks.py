import xml.etree.ElementTree as ET

class Definition(object):

    def __init__(self, definition_root):
        self._definition_root = definition_root

    def type_name(self):
        type_id = self._definition_root.find('Id').find('TypeId')
        subtype_id = self._definition_root.find('Id').find('SubtypeId')

        if type_id is None or not type_id.text:
            return subtype_id.text
        elif subtype_id is None or not subtype_id.text:
            return type_id.text
        else:
            return type_id.text + ':' + subtype_id.text

    @property
    def build_time(self):
        time = self._definition_root.find('BuildTimeSeconds')
        if time is not None:
            return float(time.text)

    @build_time.setter
    def build_time(self, value):
        time = self._definition_root.find('BuildTimeSeconds')
        if time is None:
            time = ET.SubElement(self._definition_root, 'BuildTimeSeconds')
        time.text = str(value)

    @property
    def disassembly_ratio(self):
        ratio = self._definition_root.find('DisassembleRatio')
        if ratio is not None:
            return float(ratio.text)
        return 1

    @disassembly_ratio.setter
    def disassembly_ratio(self, value):
        ratio = self._definition_root.find('DisassembleRatio')
        if ratio is None:
            ratio = ET.SubElement(self._definition_root, 'DisassembleRatio')
        ratio.text = str(value)
        