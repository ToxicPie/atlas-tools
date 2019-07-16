#!/usr/bin/env python3

# Copyright (C) 2019 Kent / toxicpie
# MIT-Licensed
#
# This script contains the essential functions that allows the parsing of a libgdx
# .atlas file.
# If is run directly, it takes an input file which is specified as a command-line
# argument (or given from stdin), then prints the parsed data as a json string.


import os, sys, re, copy, json


# regex patterns for parsing
ATLAS_PATTERN = {
    'GLOBAL_ATTRIBUTE': '^([a-z]+): (.+)$',
    'SPRITE_NAME': '^[a-zA-Z0-9-_]+$',
    'SPRITE_ATTRIBUTE': '^ +([a-z]+): (.+)$'
}


# an object representing the data of a sprite
class SpriteData:

    # empty constructor
    def __init__(self):
        self.name = ''
        self.rotate = False
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.orig_w = 0
        self.orig_h = 0
        self.offset_x = 0
        self.offset_y = 0

    # converts the object to a json string
    def to_json(self):
        return json.dumps(self.__dict__)


# an object representing the data of a sprite sheet
class SheetData:

    # empty constructor
    def __init__(self):
        self.filename = ""
        self.width = 0
        self.height = 0
        self.sprites_data = []

    # add an sprite entry to the sheet(if it exists)
    def add_sprite(self, data=None):
        if data != None:
            self.sprites_data.append(data)

    # converts the object to a dict
    def to_dict(self):
        self_copy = copy.deepcopy(self)
        self_copy.sprites_data = [x.__dict__ for x in self.sprites_data]
        return self_copy.__dict__

    # converts the object to a json string
    def to_json(self):
        self_copy = copy.deepcopy(self)
        self_copy.sprites_data = [x.__dict__ for x in self.sprites_data]
        return json.dumps(self_copy.__dict__, indent=4, sort_keys=True)
        # python automatically frees the memory here(hopefully)


# returns a list of entries, each of which containing the data of a texture sheet
def parse_atlas(file_contents):

    # divide content into blocks
    content_blocks = file_contents.split('\n\n')
    # data to return
    parsed_data = []

    for block in content_blocks:
        if block == '':
            # omit empty blocks
            continue
        else:
            content_lines = block.split('\n')

        # each block represents data of an image sheet
        image_data = SheetData()
        # first line of each block is always the file name
        image_data.filename = content_lines[1]

        current_sprite = None

        for line in content_lines:

            # process each line according to its format
            if re.search(ATLAS_PATTERN['GLOBAL_ATTRIBUTE'], line):
                # format: 'key: value'
                match = re.search(ATLAS_PATTERN['GLOBAL_ATTRIBUTE'], line)
                # get attribut key/value pair
                # note: some attributes are not used in this script, e.g. filters
                attr_key, attr_value = match.group(1), match.group(2)

                if attr_key == 'size':
                    # format: 'size: 100,200'
                    image_data.width = int(attr_value.split(',')[0])
                    image_data.height = int(attr_value.split(',')[1])

            elif re.search(ATLAS_PATTERN['SPRITE_NAME'], line):
                # beginning of a new sprite, save old one if it exists
                image_data.add_sprite(current_sprite)
                current_sprite = SpriteData()

                # the whole line is its name
                current_sprite.name = line

            elif re.search(ATLAS_PATTERN['SPRITE_ATTRIBUTE'], line):
                # format: '  key: value'
                match = re.search(ATLAS_PATTERN['SPRITE_ATTRIBUTE'], line)
                # get attribut key/value pair
                # note: some attributes are not used in this script, e.g. 9-patch stuff
                attr_key, attr_value = match.group(1), match.group(2)

                if attr_key == 'rotate':
                    # format: '  rotate: true|false'
                    current_sprite.rotate = (attr_value == 'true')

                if attr_key == 'xy':
                    # format: '  xy: 300, 400'
                    current_sprite.x = int(attr_value.split(', ')[0])
                    current_sprite.y = int(attr_value.split(', ')[1])

                if attr_key == 'size':
                    # format: '  size: 100, 200'
                    current_sprite.width = int(attr_value.split(', ')[0])
                    current_sprite.height = int(attr_value.split(', ')[1])

                if attr_key == 'offset':
                    # format: '  offset: 10, 20'
                    current_sprite.offset_x = int(attr_value.split(', ')[0])
                    current_sprite.offset_y = int(attr_value.split(', ')[1])

                if attr_key == 'orig':
                    # format: '  orig: 120, 240'
                    current_sprite.orig_w = int(attr_value.split(', ')[0])
                    current_sprite.orig_h = int(attr_value.split(', ')[1])

                if attr_key == 'index':
                    # format: '  index: 8'
                    # note: to handle indices, a suffix '.%d' is added to the name
                    if attr_value != '-1':
                        current_sprite.name += '.' + attr_value

        # whole block is read, save the last sprite
        image_data.add_sprite(current_sprite)

        # add this sheet to the list
        parsed_data.append(image_data)

    return parsed_data


# main
if __name__ == '__main__':

    # this script takes exactly 1 argument
    if len(sys.argv) != 2:
        print('Usage: {0} <input_file>'.format(sys.argv[0]))
        print('Loads a file containing libgdx texture data(.atlas) and outputs the parsed data as a pretty-printed json string. If input_file is `-`, reads from stdin instead.')
        exit()

    # attempt to read file
    if sys.argv[1] == '-':
        file_contents = sys.stdin.read()
    elif os.path.isfile(sys.argv[1]):
        try:
            input_file = open(sys.argv[1], 'r')
            file_contents = input_file.read()
        except Exception as e:
            print('FATAL: cannot load file {0}: {1}'.format(sys.argv[1], str(e)))
            exit()
        else:
            input_file.close()
    else:
        print('FATAL: cannot load file {0}: it doesn\'t exist'.format(sys.argv[1]))
        exit()

    # convert parsed data to json and print it
    parsed_data = parse_atlas(file_contents)
    parsed_data_dict = [x.to_dict() for x in parsed_data]
    print(json.dumps(parsed_data_dict, indent=4, sort_keys=True))
