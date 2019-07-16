# atlas-tools

Some scripts that may come in handy when dealing with libgdx textures.

# Usage

These scripts use Python 3.x. You have to install the Pillow module before handling images.

1. Parsing a .atlas file

    `python parser.py <input_file>`  
    Parses the given .atlas file and returns a JSON string containing its data. If `input_file` is `-`, reads from stdin instead.

2. Pack all given images into a .atlas

    TODO

3. Pack images into texture sheet(s) using given .atlas

    `python pack.py <input_file> <source_path>`  
    Reads the atlas file and updates the texture sheet by repacking everything matching `source_path/spritename.png`.

4. Unpack images from texture sheet(s) using given .atlas

    `python unpack.py <input_file> <destination_path>`  
    Reads the atlas file and saves each sprite image as an individual PNG file inside the destination path.
