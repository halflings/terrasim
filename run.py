import pyglet

from graphics import Viewport
from world import World, Cell


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


class MainWindow(pyglet.window.Window):
    DEFAULT_WORLD_SIZE = 35
    BASE_DISPLACEMENT = 25
    MOTION_DISPLACEMENTS = {pyglet.window.key.MOTION_RIGHT: (+BASE_DISPLACEMENT, 0), pyglet.window.key.MOTION_LEFT: (
        -BASE_DISPLACEMENT, 0), pyglet.window.key.MOTION_UP: (0, +BASE_DISPLACEMENT), pyglet.window.key.MOTION_DOWN: (0, -BASE_DISPLACEMENT)}

    def __init__(self, width=800, height=600):
        super().__init__(width=width, height=height)
        self.fps_display = pyglet.clock.ClockDisplay()
        self.viewport = Viewport(self, (width, height))
        self.x, self.y = 0, 0

        # World/map management
        self.world = World(width=self.DEFAULT_WORLD_SIZE, height=self.DEFAULT_WORLD_SIZE)
        self.world_view = WorldView(self, self.world)

        # Various graphical details
        sword_image = pyglet.resource.image('res/img/shortsword.png')
        sword_cursor = pyglet.window.ImageMouseCursor(
            sword_image, sword_image.width, sword_image.height)
        self.set_mouse_cursor(sword_cursor)
        self.label = pyglet.text.Label('Debug',
                                       color=(255, 255, 255, 125),
                                       font_size=12,
                                       x=self.width - 10, y=20,
                                       anchor_x='right', anchor_y='center')

    def on_draw(self):
        self.clear()
        Viewport.set_camera(self.x, self.y)
        with self.viewport:
            self.world_view.draw()
        self.label.draw()
        self.fps_display.draw()

    def on_key_press(self, symbol, modifiers):
        print('A keyboard key was pressed.')
        if symbol == pyglet.window.key.ESCAPE:
            self.on_close()

    def on_text_motion(self, motion):
        self.x += self.MOTION_DISPLACEMENTS[motion][0]
        self.y += self.MOTION_DISPLACEMENTS[motion][1]

    def on_mouse_press(self, x, y, button, modifiers):
        print('Mouse pressed on coordinates ({}, {})'.format(x, y))

    def on_mouse_motion(self, x, y, dx, dy):
        self.world_view.set_cursor_position(self.x + x, self.y + y)


if __name__ == '__main__':
    window = MainWindow()
    pyglet.app.run()
