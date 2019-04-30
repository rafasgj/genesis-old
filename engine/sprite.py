"""Define the Sprite class."""

import pygame
from .lib.GIFImage import GIFImage
from .lib.shadows import add_shadow


class Sprite:
    """Define a game sprite."""

    def __init__(self, image, **kw):
        """Initialize a sprite object."""
        scale = self.__scale = kw.get('scale', 1)
        ang = self.__rotation = kw.get('rotate', 0)
        self.__animate = kw.get('animate', False)
        self.__shadow = kw.get('shadow', None)
        if self.__animate:
            self.__image = GIFImage(image, **kw)
            x, y, w, h = self.__image.get_rect()
        else:
            self.__image = pygame.image.load(image)
            _, _, w, h = self.__image.get_rect()
            w *= scale
            h *= scale
            cx, cy = self.__image.get_rect().center
            self.__image = pygame.transform.rotozoom(self.__image, ang, scale)
            x, y, a, b = self.__image.get_rect(center=(cx, cy))
            self.__image.get_rect().center = (x + a // 2, y + b // 2)
            blt = self.__image
            if self.__shadow:
                offset, scale, amb = self.__shadow
                blt = add_shadow(blt, offset, shadow_scale=scale, ambience=amb)
            self.__image = blt
        self.__bounds = (x, y, w, h, ang, scale)

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
        return self.__bounds

    @property
    def center(self):
        """Return  sprite center."""
        return self.__image.get_rect().center

    @property
    def duration(self):
        """Retrieve animation duration, in miliseconds."""
        if self.__animate:
            return self.__image.duration()
        else:
            return 0

    @property
    def scale(self):
        """Return the scale applied to the original image."""
        return self.__scale

    @property
    def rotation(self):
        """Return the rotation applied to the original image."""
        return self.__rotation
