"""Define the Sprite class."""

import pygame
from .lib.GIFImage import GIFImage


class Sprite:
    """Define a game sprite."""

    def __init__(self, image, speed=1, animate=False, **kw):
        """Initialize a sprite object."""
        if animate:
            self.__image = GIFImage(image, **kw)
        else:
            scale = kw.get('scale', 1)
            rotate = kw.get('rotate', 0)
            self.__image = pygame.image.load(image)
            if scale != 1:
                w, h = self.__image.get_size()
                scale = (int(w * scale), int(h * scale))
                self.__image = pygame.transform.scale(self.__image, scale)
                self.__image = pygame.transform.rotate(self.__image, rotate)
        self.__animate = animate

    def draw(self, screen, position):
        """Draw the sprite to the screen."""
        pos = list(map(int, position))
        if self.__animate:
            self.__image.draw(screen, pos)
        else:
            screen.blit(self.__image, pos)

    @property
    def bounds(self):
        """Compute sprite bounds."""
        return self.__image.get_rect()
