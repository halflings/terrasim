"""
    Open-source viewport by Benjamin Moran: https://bitbucket.org/snippets/treehousegames/g6Xdg
"""

from pyglet.gl import *


class Viewport:

    def __init__(self, target_window, resolution, smoothed=False):
        """Create a fixed resolution viewport that maintains aspect ratio.

        Create a fixed resolution viewport that maintains aspect ratio, even
        when the Window is resized. Pillars or Letterboxes will appear
        as necessary.
        :param target_window: The pyglet Window instance.
        :param resolution: The target resolution as a tuple (x, y)
        :param smoothed: Whether or not you want bilinear smoothing.
        """
        self.window = target_window
        self.width = resolution[0]
        self.height = resolution[1]
        self.texture = pyglet.image.Texture.create(self.width, self.height)

        if not smoothed:
            glTexParameteri(self.texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameteri(self.texture.target, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    def __enter__(self):
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.width, 0, self.height, -1, 1)
        glMatrixMode(GL_MODELVIEW)

    @staticmethod
    def set_camera(x=0, y=0, z=0):
        """Offset the camera before blitting scrolling things."""
        glLoadIdentity()
        # Clamp to integers to prevent sprite artifacts:
        glTranslatef(int(-x), int(-y), int(-z))

    @staticmethod
    def reset_camera():
        """Reset the camera to zero before blitting static things (hud)."""
        glLoadIdentity()

    def __exit__(self, *unused_args):
        """Blit the frambuffer to the Window.

        Aspect ratio is preserved, and the final image will be letterboxed
        or pillared, as appropriate. The Window can be resized freely.
        """
        window = self.window
        width = self.width
        height = self.height
        buffer = pyglet.image.get_buffer_manager().get_color_buffer()
        self.texture.blit_into(buffer, 0, 0, 0)

        glViewport(0, 0, window.width, window.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, window.width, 0, window.height, -1, 1)
        glMatrixMode(GL_MODELVIEW)

        aspect_width = window.width / width
        aspect_height = window.height / height

        # Create letterbox/pillar effect when resizing window:
        if aspect_width > aspect_height:
            scale_width = aspect_height * width
            scale_height = aspect_height * height
        else:
            scale_width = aspect_width * width
            scale_height = aspect_width * height
        x = (window.width - scale_width) / 2
        y = (window.height - scale_height) / 2

        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        glColor3f(1, 1, 1)
        self.texture.blit(x, y, width=scale_width, height=scale_height)

    def begin(self):
        self.__enter__()

    def end(self):
        self.__exit__()
