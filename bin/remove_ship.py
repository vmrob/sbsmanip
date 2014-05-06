#!/usr/local/bin/python

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
        subtype_name = block.find('SubtypeName')
        builder_name = block.get(
            '{http://www.w3.org/2001/XMLSchema-instance}type')
        if subtype_name is not None and subtype_name.text is not None:
            block_list.append(subtype_name.text)
        elif builder_name is not None:
            block_list.append(builder_name)
        else:
            block_list.append('Unknown block')
    return block_list

target_ship_parts = ship_part_list(
    target_ship.find('CubeBlocks').findall('MyObjectBuilder_CubeBlock'))

tree = ET.parse(filename)
root = tree.getroot()

entities = root.find('SectorObjects')

delete_queue = []

for entity in entities.findall('MyObjectBuilder_EntityBase'):
    if entity.get('{http://www.w3.org/2001/XMLSchema-instance}type') != \
            'MyObjectBuilder_CubeGrid':
        continue

    entity_id = entity.find('EntityId').text

    blocks = entity.find('CubeBlocks').findall('MyObjectBuilder_CubeBlock')

    block_list = ship_part_list(blocks)

    if set(block_list) == set(target_ship_parts):
        print 'entity %s matches target with %d parts' % (entity_id,
                                                          len(block_list))
        delete_queue.append(entity)

if len(delete_queue) > 0:
    response = raw_input('delete these %d objects? [y/n]' % len(delete_queue))

    if response == 'y' or response == 'Y':
        for entity in delete_queue:
            entities.remove(entity)
        tree.write(filename)
else:
    print 'no ships match the filter' 