"""Define the Sprite class."""

import pygame
from .lib.GIFImage import GIFImage


class Sprite(object):
    """Define a game sprite."""

    def __init__(self, image, pos, speed=1, animate=False, **kwargs):
        """Initialize a sprite object."""
        self.__pos = pos
        if animate:
            self.__image = GIFImage(image, **kwargs)
        else:
            scale = kwargs.get('scale', 1)
            rotate = kwargs.get('rotate', 0)
            self.__image = pygame.image.load(image)
            if scale != 1:
                w, h = self.__image.get_size()
                scale = (int(w * scale), int(h * scale))
                self.__image = pygame.transform.scale(self.__image, scale)
                self.__image = pygame.transform.rotate(self.__image, rotate)
        self.__speed = speed
        self.move = (0, 0)
        self.__animate = animate
        self.__visible = True

    def draw(self, screen):
        """Draw the sprite to the screen."""
        if self.__animate:
            self.__image.draw(screen, self.__pos)
        else:
            screen.blit(self.__image, self.__pos)

    def update(self):
        """Update sprite position."""
        x, y = self.__pos
        dx, dy = self.move
        speed = self.__speed
        self.__pos = (x + dx * speed, y + dy * speed)

    def limits(self, window):
        """Ensure sprite in within limits."""
        w, h = window
        a, b = self.__image.get_size()
        x, y = self.__pos
        x = 0 if x < 0 else w - a if x > w - a else x
        y = 0 if y < 0 else h - b if y > h - b else y
        self.__pos = (x, y)

    @property
    def center(self):
        """Compute the certer of the sprite, based on its size."""
        x, y = self.__pos
        _, _, w, h = self.__image.get_rect()
        return (x + w // 2, y + h // 2)

    @property
    def bounds(self):
        """Compute sprite bounds."""
        x, y = self.__pos
        _, _, w, h = self.__image.get_rect()
        return (x, y, w, h)

    @property
    def length(self):
        """Return the time needed to draw the animation."""
        return self.__image.duration() if self.__animate else 0

    def hide(self):
        """Set Game Object to invisible."""
        self.__visible = False
