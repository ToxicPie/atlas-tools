#!/usr/bin/env python3

# Copyright (C) 2019 Kent / toxicpie
# MIT-Licensed
#
# This script reads a libgdx texture atlas file, load sprite from texture sheets,
# then saves each sprite as a seperate png in the destination directory.


import os, sys
from PIL import Image

import parser


# main
if __name__ == '__main__':

    # this script takes exactly 2 arguments
    # if the count doesn't match, prints some usage hints
    if len(sys.argv) != 3:
        print('Usage: {0} <input_file> <destination_path>'.format(sys.argv[0]))
        print('Loads a file containing libgdx texture data(.atlas) and save each sprite as an individual image into the destination directory.')
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

    # check if destination path exists; if not, create one
    if os.path.isdir(sys.argv[2]):
        print('Directory {0} already exists.'.format(sys.argv[2]))
    else:
        try:
            os.makedirs(sys.argv[2])
        except Exception as e:
            print('FATAL: cannot create directory \'{0}\': {1}'.format(sys.argv[2], str(e)))
            exit()
        else:
            print('Created destination directory {0}.'.format(sys.argv[2]))
    destination_path = os.path.normpath(sys.argv[2])

    # parse data using parser.py
    parsed_data = parser.parse_atlas(file_contents)

    # an atlas can contain multiple texture sheets
    for sheet in parsed_data:

        # read image file
        try:
            sheet_path = os.path.join(os.path.dirname(sys.argv[1]), sheet.filename)
            sheet_image = Image.open(sheet_path)
        except Exception as e:
            # skip current sheet if there's a problem opening the image
            print('ERROR: cannot open image \'{0}\': {1}'.format(sheet.filename, str(e)))
            continue
        else:
            print('Loaded image {0}.'.format(sheet.filename))

        for sprite in sheet.sprites_data:

            # get cropped region of the sprite
            sprite_image = Image.new('RGBA', (sprite.orig_w, sprite.orig_h), (0, 0, 0, 0))
            sprite_region = (sprite.x, sprite.y, sprite.x + sprite.width, sprite.y + sprite.height)
            sprite_cropped = sheet_image.crop(sprite_region)
            sprite_image.paste(sprite_cropped, (sprite.offset_x, sprite.offset_y))

            if sprite.rotate:
                sprite_image = sprite_image.transpose(Image.ROTATE_90)

            # save sprite image file
            sprite_filename = os.path.join(destination_path, sprite.name + '.png')
            try:
                sprite_image.save(sprite_filename)
            except Exception as e:
                # skip current sprite if there's a problem saving the image
                print('ERROR: cannot save image \'{0}\': {1}'.format(sprite_filename, str(e)))
                continue
            else:
                print('Saved image {0}.'.format(sprite_filename))
