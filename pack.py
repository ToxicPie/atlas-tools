#!/usr/bin/env python3

# Copyright (C) 2019 Kent / toxicpie
# MIT-Licensed
#
# This script reads a libgdx texture atlas file, load sprites from the source
# directory, then pack them into texture sheets.


import os, sys
from PIL import Image

import parser


# main
if __name__ == '__main__':

    # this script takes exactly 2 arguments
    # if the count doesn't match, prints some usage hints
    if len(sys.argv) != 3:
        print('Usage: {0} <input_file> <source_path>'.format(sys.argv[0]))
        print('Loads a file containing libgdx texture data(.atlas) and packs all sprites from the source dirctory into texture sheets.')
        exit()

    # try to read data from atlas file
    try:
        input_file = open(sys.argv[1], 'r')
        file_contents = input_file.read()
    except Exception as e:
        print('FATAL: cannot open file \'{0}\': {1}'.format(sys.argv[0], str(e)))
        exit()
    else:
        input_file.close()
        print('File {0} loaded successfully.'.format(sys.argv[1]))

    # check if source path exists
    if not os.path.isdir(sys.argv[2]):
        print('FATAL: cannot open directory \'{0}\': {1}'.format(sys.argv[2], str(e)))
        exit()
    destination_path = os.path.normpath(sys.argv[2])

    # parse data using parser.py
    parsed_data = parser.parse_atlas(file_contents)

    # an atlas can contain multiple texture sheets
    for sheet in parsed_data:

        # create empty sheet
        sheet_image = Image.new('RGBA', (sheet.width, sheet.height), (0, 0, 0, 0))

        for sprite in sheet.sprites_data:

            # load sprite image file
            sprite_filename = destination_path + '/' + sprite.name + '.png'
            try:
                sprite_image = Image.open(sprite_filename)
            except Exception as e:
                # skip current sprite if there's a problem saving the image
                print('ERROR: cannot load image \'{0}\': {1}'.format(sprite_filename, str(e)))
                continue
            else:
                print('Loaded image {0}.'.format(sprite_filename))

            if sprite.rotate:
                sprite_image = sprite_image.transpose(Image.ROTATE_270)

            # paste sprite onto the sheet
            sprite_region = (sprite.offset_x, sprite.offset_y, sprite.offset_x + sprite.width, sprite.offset_y + sprite.height)
            sprite_cropped = sprite_image.crop(sprite_region)
            sheet_image.paste(sprite_cropped, (sprite.x, sprite.y))

        # read image file
        try:
            sheet_image.save(sheet.filename)
        except Exception as e:
            # skip current sheet if there's a problem opening the image
            print('ERROR: cannot save image \'{0}\': {1}'.format(sheet.filename, str(e)))
            continue
        else:
            print('Saved image {0}.'.format(sheet.filename))
