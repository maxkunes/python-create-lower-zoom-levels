import math
import os.path
from PIL import Image
import pathlib

# NOTE: if you map isn't square, rename the tile folder to one zoom level
# above the actual zoom level. In this zoom level, if tiles when found that are
# expected they will be replaced properly with the below placeholder image
# of a base color (or whatever you want)

placeholder_img = Image.new("RGB", (256, 256), (255, 255, 255))


def get_tile(zoom, col, row):
    p = '{}/{}/{}.jpg'.format(zoom, col, row)

    if not os.path.isfile(p):
        path = pathlib.Path(p)
        path.parent.mkdir(parents=True, exist_ok=True)
        placeholder_img.save(p, quality=100)
        print('{} not found, using placeholder...'.format(p))
        return 'placeholder'
        #raise ValueError('{} does not exist!'.format(p))
    
    return p

def open_image(path):

    if path == 'placeholder':
        return placeholder_img.resize((128, 128))

    return Image.open(path).resize((128, 128))

def make_tile(zoom, col, row, tl, bl, tr, br):



    tile = Image.new('RGB', (256, 256))

    tile.paste(open_image(tl), (0,0))
    tile.paste(open_image(bl), (0,128))
    tile.paste(open_image(tr), (128,0))
    tile.paste(open_image(br), (128,128))

    p = '{}/{}/{}.jpg'.format(zoom, col, row)

    path = pathlib.Path(p)
    path.parent.mkdir(parents=True, exist_ok=True)

    tile.save(p, quality=100)

    pass

def gen_lower_zoom_level(base_zoom_level):

    # number of items (folders of cols, num images per col (rows))
    num_items = pow(2, base_zoom_level)

    col_idx = 0

    while col_idx < num_items:

        # to merge to a lower zoom level we need to make an image out of the
        # following things:

        # col_idx at row_idx == top left of new image
        # col_idx at row_idx + 1 == bottom left of new image

        # col_idx + 1 at row_idx == top right of new image
        # col_idx + 1 at row_idx + 1 == bottom right of new image

        row_idx = 0
        
        while row_idx < num_items:
            top_left = get_tile(base_zoom_level, col_idx, row_idx)
            bot_left = get_tile(base_zoom_level, col_idx, row_idx + 1)

            top_right = get_tile(base_zoom_level, col_idx + 1, row_idx)
            bot_right = get_tile(base_zoom_level, col_idx + 1, row_idx + 1)

            new_col_idx = col_idx / 2 # implicit floor here
            new_row_idx = row_idx / 2 # implicit floor here

            make_tile(base_zoom_level - 1, int(new_col_idx), int(new_row_idx),
                top_left, bot_left, top_right, bot_right)

            print('Created {}/{}/{}.jpg'.format(base_zoom_level - 1, int(new_col_idx), int(new_row_idx)))

            row_idx+=2

        col_idx += 2


zoom_level = 7

while zoom_level > 0:

    gen_lower_zoom_level(zoom_level)

    zoom_level -= 1