import pyglet

from constants import BASE_DISPLACEMENT, UPDATE_RATE
from game import Game
from graphics import Viewport
from views import WorldView


class MainWindow(pyglet.window.Window):
    DEFAULT_WORLD_SIZE = 35
    MOTION_DISPLACEMENTS = {pyglet.window.key.MOTION_RIGHT: (+BASE_DISPLACEMENT, 0),
                            pyglet.window.key.MOTION_LEFT: (-BASE_DISPLACEMENT, 0),
                            pyglet.window.key.MOTION_UP: (0, +BASE_DISPLACEMENT),
                            pyglet.window.key.MOTION_DOWN: (0, -BASE_DISPLACEMENT)}

    def __init__(self, width=800, height=600):
        super().__init__(width=width, height=height)
        self.fps_display = pyglet.clock.ClockDisplay()
        self.viewport = Viewport(self, (width, height))
        self.x, self.y = 0, 0

        # World/map management
        self.game = Game()
        self.world_view = WorldView(self, self.game.world)

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

        # Setting a clock for updating the state of the game
        pyglet.clock.schedule_interval(self.update, UPDATE_RATE)

    def update(self, dt):
        self.game.update(dt)

    def on_draw(self):
        self.clear()
        Viewport.set_camera(self.x, self.y)
        with self.viewport:
            self.world_view.draw()
        self.label.draw()
        self.fps_display.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            self.on_close()

    def on_text_motion(self, motion):
        self.x += self.MOTION_DISPLACEMENTS[motion][0]
        self.y += self.MOTION_DISPLACEMENTS[motion][1]

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        self.world_view.set_cursor_position(self.x + x, self.y + y)


if __name__ == '__main__':
    window = MainWindow()
    pyglet.app.run()
