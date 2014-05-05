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
    print 'usage: remove_debris [filename] [minimum block count]'
    print '  minimum block count is the minimum number of blocks required'
    print '  for a ship or station to not be considered debris. For example'
    print '  minimum block count of 3 would erase all ships with less than 3'
    print '  blocks attached to it.'
    exit(1)

filename = sys.argv[1]
min_block_count = int(sys.argv[2])

tree = ET.parse(filename)
root = tree.getroot()

delete_queue = []

entities = root.find('SectorObjects')

for entity in entities.findall('MyObjectBuilder_EntityBase'):
    if entity.get('{http://www.w3.org/2001/XMLSchema-instance}type') != 'MyObjectBuilder_CubeGrid':
        continue

    entity_id = entity.find('EntityId').text

    blocks = entity.find('CubeBlocks').findall('MyObjectBuilder_CubeBlock')

    if len(blocks) < min_block_count:
        beacon_present = False
        reactor_present = False
        blocklist = []
        for block in blocks:
            custom_name = block.find('CustomName')
            subtype_name = block.find('SubtypeName')
            builder_name = block.get('{http://www.w3.org/2001/XMLSchema-instance}type')
            if builder_name == 'MyObjectBuilder_Beacon':
                beacon_present = True
            if builder_name == 'MyObjectBuilder_Reactor':
                reactor_present = True
            if custom_name is not None and custom_name.text is not None:
                blocklist.append(custom_name.text)
            elif subtype_name is not None and subtype_name.text is not None:
                blocklist.append(subtype_name.text)
            elif builder_name is not None:
                blocklist.append(builder_name)
            else:
                blocklist.append('Unknown block')
        if reactor_present and beacon_present:
            print 'excluding entity %s because it contains beacon + reactor:\n%s' % (entity_id, ',\n'.join(blocklist))
        else:
            delete_queue.append(entity)
            print 'entity %s contains %d blocks\n%s' % (entity_id, len(blocks), ',\n'.join(blocklist))

if len(delete_queue) > 0:
    response = raw_input('delete these %d objects? [y/n]' % len(delete_queue))

    if response == 'y' or response == 'Y':
        for entity in delete_queue:
            entities.remove(entity)
        tree.write(filename)
else:
    print 'no entities contain less than %d blocks' % min_block_count 