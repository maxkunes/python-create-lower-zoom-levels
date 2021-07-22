# python-create-lower-zoom-levels

Just a simple script to take a zoom/col/row.jpg (leaflet style) formatted tiled map and create lower zoom levels from a single higher zoom level.

Deps:
Python3 and PIL

License:
MIT

This script only technically supports a tiled map with the same rows as columns aka. a square map. This simplifies things greatly for the script and custom tile map renderers.
To somewhat support a non-square map, you can copy a version of your tile folder and effectively rename it to the next highest zoom level in which the widest side of the map
can fit in, or if the rectangular map does not fully fit in the current zoom level, you can leave it as it is. If the script parses this map, it assumes it is square. If the map
is rectangular, the script will automatically replace/add any missing tiles with a placeholder tile defined at the top of the script. In this script by default, that tile is white. 
Doing this will effectively make the map square by filling in any empty area with placeholder tiles. Using a custom/extendable tile renderer, one could exclude these tiles from rendering to prevent any outline of sorts.
