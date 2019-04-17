"""Models an explosion."""

from engine import GameObject, Sprite, Hideable

import pygame


class Explosion(Hideable, GameObject):
    """Model a temporary explosion."""

    BIG = "media/images/explosao.gif"
    SMALL = "media/images/explosion.gif"

    def __init__(self, position, type=SMALL, **kwargs):
        """Initialize the object."""
        Hideable.__init__(self)
        GameObject.__init__(self, GameObject.Priority.DEFAULT)
        ts = kwargs.get('time_scale', 1.0)
        self.__sprite = Sprite(type, animate=True, time_scale=ts, loop=True)
        self.__ttl = self.__sprite.duration + pygame.time.get_ticks()
        _, _, w, h = list(map(lambda i: i // 2, self.__sprite.bounds))
        x, y = position
        self.__position = (x - w, y - h)

    def update(self, bounds):
        """Update object."""
        if pygame.time.get_ticks() > self.__ttl:
            self.hide()

    def draw(self, screen):
        """Draw object."""
        self.__sprite.draw(screen, self.__position)
