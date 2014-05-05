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
    print 'usage: remove_ship.py [filename] [definition file]'
    exit(1)

filename = sys.argv[1]
def_file = sys.argv[2]

target_tree = ET.parse(def_file)
target_ship = target_tree.getroot()

def ship_part_list(blocks):
    block_list = []
    for block in blocks:
        #custom_name = block.find('CustomName')
        subtype_name = block.find('SubtypeName')
        builder_name = block.get('{http://www.w3.org/2001/XMLSchema-instance}type')
        if subtype_name is not None and subtype_name.text is not None:
            block_list.append(subtype_name.text)
        elif builder_name is not None:
            block_list.append(builder_name)
        else:
            block_list.append('Unknown block')
    return block_list

target_ship_parts = ship_part_list(target_ship.find('CubeBlocks').findall('MyObjectBuilder_CubeBlock'))

# print 'target ship contains %d parts: \n%s' % (len(target_ship_parts), ',\n'.join(target_ship_parts))

tree = ET.parse(filename)
root = tree.getroot()

entities = root.find('SectorObjects')

delete_queue = []

for entity in entities.findall('MyObjectBuilder_EntityBase'):
    if entity.get('{http://www.w3.org/2001/XMLSchema-instance}type') != 'MyObjectBuilder_CubeGrid':
        continue

    entity_id = entity.find('EntityId').text

    blocks = entity.find('CubeBlocks').findall('MyObjectBuilder_CubeBlock')

    block_list = ship_part_list(blocks)

    if set(block_list) == set(target_ship_parts):
    	print 'entity %s matches target with %d parts' % (entity_id, len(block_list))
        delete_queue.append(entity)

if len(delete_queue) > 0:
    response = raw_input('delete these %d objects? [y/n]' % len(delete_queue))

    if response == 'y' or response == 'Y':
        for entity in delete_queue:
            entities.remove(entity)
        tree.write(filename)
else:
    print 'no ships match the filter' 