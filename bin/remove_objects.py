#!/usr/local/bin/python

import math
import sys

import xml.etree.ElementTree as ET

xmlfile = ''

if len(sys.argv) != 3:
    print 'usage: remove_objects.py [filename] [distance]'
    exit(1)

filename = sys.argv[1]
max_distance = int(sys.argv[2])

tree = ET.parse(filename)
root = tree.getroot()

delete_queue = []

entities = root.find('SectorObjects')

for entity in entities.findall('MyObjectBuilder_EntityBase'):
    entity_id = entity.find('EntityId').text

    position = entity.find('PositionAndOrientation').find('Position')

    x = float(position.get('x'))
    y = float(position.get('y'))
    z = float(position.get('z'))

    dist = math.sqrt(x**2 + y**2 + z**2)

    if dist > max_distance:
        delete_queue.append(entity)
        print ('entity %s (%.0f, %.0f, %.0f), '
               'distance of %.0f' % (entity_id, x, y, z, dist))

if len(delete_queue) > 0:
    response = raw_input('delete these %d objects? [y/n]' % len(delete_queue))

    if response == 'y' or response == 'Y':
        for entity in delete_queue:
            entities.remove(entity)
        tree.write(filename)
else:
    print 'no objects farther than a distance of %.0f' % max_distance 