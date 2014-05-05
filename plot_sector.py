# The MIT License (MIT)
#
# Copyright (c) 2014 Victor Robertson
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import re
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