#!/usr/local/bin/python

import sys

import xml.etree.ElementTree as ET

xmlfile = ''

if len(sys.argv) != 2:
    print 'usage: count_objects [filename]'
    exit(1)

filename = sys.argv[1]

tree = ET.parse(filename)
root = tree.getroot()

print 'there are %d objects in the sector' % len(
    root.find('SectorObjects').findall('MyObjectBuilder_EntityBase'))
