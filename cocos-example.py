import cocos
from cocos.tiles import TileSet, RectCell, RectMapLayer
from cocos.director import director
from cocos.layer.scrolling import ScrollingManager
import pyglet

from world import Cell

CELL_TEXTURES = {Cell.GRASS: 'grass.png', Cell.DIRT: 'dirt.png', Cell.WATER: 'water.png',
                 Cell.MOUNTAIN: 'mountain.png'}
CELL_SIZE = 32


class GeneratedMap(RectMapLayer):

    def __init__(self, width, height, id=0):
        cells = self._generate_cells(width, height, CELL_SIZE)
        super(GeneratedMap, self).__init__(id=id, tw=CELL_SIZE, th=CELL_SIZE, cells=cells)

    def _generate_cells(self, width, height, cell_size):
        tileset = TileSet(0, None)
        for cell_type in list(Cell):
            image_path = 'res/img/tiles/{}'.format(CELL_TEXTURES[cell_type])
            image = pyglet.resource.image(image_path)
            tileset.add(image=image, id=cell_type, properties={})

        cells = []
        for i in range(width):
            column = []
            for j in range(height):
                tile = tileset[Cell.MOUNTAIN] if (
                    5 < i < 10 and 6 < j < 20) else tileset[Cell.DIRT]
                cell = RectCell(i, j, cell_size, cell_size, properties={}, tile=tile)
                column.append(cell)
            cells.append(column)
        return cells


if __name__ == '__main__':
    director.init(resizable=True, autoscale=False)
    scroller = ScrollingManager()
    scroller.add(GeneratedMap(100, 100))
    main_scene = cocos.scene.Scene(scroller)
    director.run(main_scene)
