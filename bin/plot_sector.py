#!/usr/local/bin/python

import sys

import xml.etree.ElementTree as ET

xmlfile = ''

if len(sys.argv) != 3:
    print 'usage: plot_sector.py [filename] [output]'
    exit(1)

filename = sys.argv[1]
outfile = sys.argv[2]

tree = ET.parse(filename)
root = tree.getroot()

entities = root.find('SectorObjects')

with open(outfile, 'w') as f:
    for entity in entities.findall('MyObjectBuilder_EntityBase'):
        entity_id = entity.find('EntityId').text

        position = entity.find('PositionAndOrientation').find('Position')

        coords = [position.get('x'), position.get('y'), position.get('z')]

        f.write('\t'.join(coords) + '\n')