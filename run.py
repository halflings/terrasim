import random

import pyglet

from constants import BASE_DISPLACEMENT, UPDATE_RATE
from game import Game
from graphics import Viewport
from views import WorldView, CharactersView


class MainWindow(pyglet.window.Window):
    DEFAULT_WORLD_SIZE = 35
    MOTION_DISPLACEMENTS = {pyglet.window.key.MOTION_RIGHT: (+1, 0),
                            pyglet.window.key.MOTION_LEFT: (-1, 0),
                            pyglet.window.key.MOTION_UP: (0, +1),
                            pyglet.window.key.MOTION_DOWN: (0, -1)}

    def __init__(self, width=800, height=600):
        super().__init__(width=width, height=height)
        self.fps_display = pyglet.clock.ClockDisplay()
        self.viewport = Viewport(self, (width, height))
        self.x, self.y = 0, 0

        # World/map management
        self.seed = random.Random()
        self.game = Game(seed=self.seed)
        self.world_view = WorldView(self, self.game.world)
        self.characters_view = CharactersView(self, self.game)

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

        # Other flags, etc.
        self.camera_speed = BASE_DISPLACEMENT

        # Setting a clock for updating the state of the game
        pyglet.clock.schedule_interval(self.update, UPDATE_RATE)

    def update(self, dt):
        self.game.update(dt)

    def on_draw(self):
        self.clear()
        Viewport.set_camera(self.x, self.y)
        with self.viewport:
            self.world_view.draw()
            self.characters_view.draw()
            self.world_view.draw_selected_cell()

        self.label.draw()
        self.fps_display.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            self.on_close()

    def on_text_motion(self, motion):
        self.x += self.MOTION_DISPLACEMENTS[motion][0] * self.camera_speed
        self.y += self.MOTION_DISPLACEMENTS[motion][1] * self.camera_speed
        self.camera_speed = min(int(self.camera_speed * 1.1), BASE_DISPLACEMENT * 3)

    def on_key_release(self, symbol, modifiers):
        self.camera_speed = BASE_DISPLACEMENT

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        self.world_view.set_cursor_position(self.x + x, self.y + y)


if __name__ == '__main__':
    window = MainWindow()
    pyglet.app.run()
