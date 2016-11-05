import pyglet

from world import Cell


class WorldView(object):
    CELL_TEXTURES = {Cell.GRASS: 'grass.png', Cell.DIRT: 'dirt.png',
                     Cell.WATER: 'water.png', Cell.MOUNTAIN: 'mountain.png'}
    CELL_SIZE = 32

    def __init__(self, window, world):
        self.window = window
        self.world = world
        self.textures = {cell_type: pyglet.resource.image(
            'res/img/tiles/{}'.format(self.CELL_TEXTURES[cell_type])) for cell_type in list(Cell)}
        self.cursor_position = None
        self.selected_cell = None

    def set_cursor_position(self, x, y):
        self.cursor_position = (x, y)
        self.selected_cell = (x // self.CELL_SIZE, y // self.CELL_SIZE)

    def draw(self):
        # Drawing all cells
        for x in range(self.world.width):
            for y in range(self.world.height):
                self.textures[self.world.cells[y][x]].blit(
                    x * self.CELL_SIZE, y * self.CELL_SIZE)

        # Drawing rectangle around the currently selected cell
        if self.selected_cell is not None:
            x, y = self.selected_cell[0] * self.CELL_SIZE, self.selected_cell[1] * self.CELL_SIZE
            dx = dy = self.CELL_SIZE
            vertices = [x, y, x + dx, y, x + dx, y + dy, x, y + dy]
            pyglet.graphics.draw(
                4, pyglet.gl.GL_LINE_LOOP, ('v2f', vertices), ('s3B', (0, 0, 255, 0, 255, 0, 255, 0, 0, 255, 255, 255)))
