#!/usr/local/bin/python

import sys

import xml.etree.ElementTree as ET

newfile = ''

if len(sys.argv) != 3:
    print 'usage: scale_world.py [filename] [scale]'
    exit(1)

filename = sys.argv[1]
scale = float(sys.argv[2])

tree = ET.parse(filename)
root = tree.getroot()

entities = root.find('SectorObjects')

for entity in entities.findall('MyObjectBuilder_EntityBase'):
    entity_id = entity.find('EntityId').text
    position = entity.find('PositionAndOrientation').find('Position')

    x = float(position.get('x')) * scale
    y = float(position.get('y')) * scale
    z = float(position.get('z')) * scale

    position.set('x', str(x))
    position.set('y', str(y))
    position.set('z', str(z))

tree.write(filename)
