import pyglet

from world import World, Cell


class WorldView(object):
    CELL_TEXTURES = {Cell.GRASS: 'grass.png', Cell.DIRT: 'dirt.png',
                     Cell.WATER: 'water.png', Cell.MOUNTAIN: 'mountain.png'}
    CELL_SIZE = 32

    def __init__(self, world):
        self.world = world
        self.textures = {cell_type: pyglet.resource.image(
            'res/img/tiles/{}'.format(self.CELL_TEXTURES[cell_type])) for cell_type in list(Cell)}

    def draw(self):
        for x in range(self.world.width):
            for y in range(self.world.height):
                self.textures[self.world.cells[y][x]].blit(
                    x * self.CELL_SIZE, y * self.CELL_SIZE)


class MainWindow(pyglet.window.Window):
    DEFAULT_WORLD_SIZE = 25

    def __init__(self, width=800, height=600):
        super().__init__(width=width, height=height)
        self.fps_display = pyglet.clock.ClockDisplay()

        # World/map management
        self.world = World(width=self.DEFAULT_WORLD_SIZE, height=self.DEFAULT_WORLD_SIZE)
        self.world_view = WorldView(self.world)

        # Various graphical details
        sword_image = pyglet.resource.image('res/img/shortsword.png')
        self.sword_sprite = pyglet.sprite.Sprite(sword_image, x=50, y=100)
        self.label = pyglet.text.Label('Debug',
                                       color=(255, 255, 255, 125),
                                       font_size=12,
                                       x=self.width - 10, y=20,
                                       anchor_x='right', anchor_y='center')

    def on_draw(self):
        self.clear()
        self.world_view.draw()
        self.sword_sprite.draw()
        self.label.draw()
        self.fps_display.draw()

    def on_key_press(self, symbol, modifiers):
        print('A keyboard key was pressed.')
        if symbol == pyglet.window.key.ESCAPE:
            self.on_close()

    def on_mouse_press(self, x, y, button, modifiers):
        print('Mouse pressed on coordinates ({}, {})'.format(x, y))

    def on_mouse_motion(self, x, y, dx, dy):
        self.sword_sprite.x = x
        self.sword_sprite.y = y


if __name__ == '__main__':
    window = MainWindow()
    pyglet.app.run()
