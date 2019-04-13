"""Define the Sprite class."""

import pygame
from .lib.GIFImage import GIFImage
from .gameobject import GameObject


class Sprite(GameObject):
    """Define a game sprite."""

    def __init__(self, image, pos, speed=1, animate=False, **kw):
        """Initialize a sprite object."""
        GameObject.__init__(self, kw.get('priority',
                                         GameObject.Priority.DEFAULT))
        self.__pos = pos
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
        self.__speed = speed
        self.move = (0, 0)
        self.__animate = animate
        self.__visible = True

    def draw(self, screen):
        """Draw the sprite to the screen."""
        pos = list(map(int, self.position))
        if self.__animate:
            self.__image.draw(screen, pos)
        else:
            screen.blit(self.__image, pos)

    def update(self):
        """Update sprite position."""
        x, y = self.__pos
        dx, dy = self.move
        self.__pos = (x + dx, y + dy)

    @property
    def position(self):
        """Retrieve the current sprite position."""
        return self.__pos

    @position.setter
    def position(self, pos):
        """Retrieve the current sprite position."""
        self.__pos = pos

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

    @property
    def speed(self):
        """Return the sprite speed."""
        return self.__speed

    def hide(self):
        """Set Game Object to invisible."""
        self.__visible = False
