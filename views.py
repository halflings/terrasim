import math

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

        self.batch = pyglet.graphics.Batch()
        self.map_sprites = []

    def set_cursor_position(self, x, y):
        self.cursor_position = (x, y)
        self.selected_cell = (x // self.CELL_SIZE, y // self.CELL_SIZE)

    def generate_sprites(self):
        min_x = max(0, self.window.x // self.CELL_SIZE)
        min_y = max(0, self.window.y // self.CELL_SIZE)
        cell_width = (self.window.width // self.CELL_SIZE) + 1
        cell_height = (self.window.height // self.CELL_SIZE) + 1
        max_x = min(min_x + cell_width, self.world.width - 1)
        max_y = min(min_y + cell_height, self.world.height - 1)

        map_sprites = []
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                sprite = pyglet.sprite.Sprite(
                    self.textures[self.world.cells[y][x]], x=x * self.CELL_SIZE, y=y * self.CELL_SIZE, batch=self.batch)
                map_sprites.append(sprite)
        return map_sprites

    def draw(self):
        self.map_sprites = self.generate_sprites()
        self.batch.draw()

        # Drawing rectangle around the currently selected cell
        if self.selected_cell is not None:
            x, y = self.selected_cell[0] * self.CELL_SIZE, self.selected_cell[1] * self.CELL_SIZE
            dx = dy = self.CELL_SIZE
            vertices = [x, y, x + dx, y, x + dx, y + dy, x, y + dy]
            pyglet.graphics.draw(
                4, pyglet.gl.GL_LINE_LOOP, ('v2f', vertices), ('s3B', (0, 0, 255, 0, 255, 0, 255, 0, 0, 255, 255, 255)))
