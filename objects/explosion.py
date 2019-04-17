"""Models an explosion."""

from engine import GameObject, Sprite, Hideable

import pygame


class Explosion(Hideable, GameObject):
    """Model a temporary explosion."""

    BIG = "media/images/explosao.gif"
    SMALL = "media/images/explosion.gif"

    def __init__(self, position, type=SMALL):
        """Initialize the object."""
        Hideable.__init__(self)
        GameObject.__init__(self, GameObject.Priority.DEFAULT)
        self.__sprite = Sprite(type, True, time_scale=1.25, loop=True)
        self.__ttl = self.__sprite.duration + pygame.time.get_ticks()
        self.__position = position

    def update(self, bounds):
        """Update object."""
        if pygame.time.get_ticks() > self.__ttl:
            self.hide()

    def draw(self, screen):
        """Draw object."""
        self.__sprite.draw(screen, self.__position)
