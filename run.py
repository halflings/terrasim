import pyglet


class MainWindow(pyglet.window.Window):

    def __init__(self, width=800, height=600):
        super().__init__(width=width, height=height)
        sword_image = pyglet.resource.image('res/img/shortsword.png')
        self.sword_sprite = pyglet.sprite.Sprite(sword_image, x=50, y=100)
        self.label = pyglet.text.Label('En garde!',
                                       color=(255, 255, 255, 125),
                                       font_size=36,
                                       x=self.width // 2, y=self.height // 2,
                                       anchor_x='center', anchor_y='center')

    def on_draw(self):
        self.clear()
        self.sword_sprite.draw()
        self.label.draw()

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
