"""The Game Window implementation."""

import pygame


class Window:
    """Abstracts a fullframe game window."""

    def __init__(self, **kwargs):
        """
        Initialize the window object.

        Optional Name Parameters:
            - x_res: screen resolution of the x axis (width).
            - y_res: screen resolution of the y axis (height).
            - size: screen resolution (w, h). Defaults to current resolution.
            - name: window name and caption.
            - cursor: True if mouse is to be shown. (Default: False)
        """
        io = pygame.display.Info()
        x_res = kwargs.get('x_res', io.current_w)
        y_res = kwargs.get('y_res', io.current_h)
        x_res, y_res = self.__dimension = kwargs.get('size', (x_res, y_res))
        name = kwargs.get('name', 'the game')
        self.__cursor = kwargs.get('cursor', False)
        pygame.mouse.set_visible(self.__cursor)
        # inicia tela
        flags = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
        self.__screen = pygame.display.set_mode(self.__dimension, flags)
        pygame.display.set_caption(name)

    def draw(self, object):
        """Asks the object to draw itself on the window canvas."""
        object.draw(self.__screen)

    def clear(self, color=(0, 0, 0)):
        """Clear the window with the given color."""
        self.__screen.fill(color)

    @property
    def size(self):
        """Retrieve the screen dimension."""
        return self.__dimension

    @property
    def display(self):
        """Retrieve the current display canvas."""
        return self.__screen

    @property
    def cursor(self):
        """Return true if the cursor is visible."""
        return self.__cursor

    @cursor.setter
    def cursor(self, on):
        """Set cursor visibility."""
        pygame.cursor.set_visible(on)
        self.__cursor = on
