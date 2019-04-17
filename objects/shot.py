"""Models a shot."""

from engine import (GameObject, Collider, Controllable, Movable, Hideable,
                    ConstantController)
import pygame
from math import atan2, pi, cos, sin


class Shot(Collider, Controllable, Movable, Hideable, GameObject):
    """Models a shot."""

    @staticmethod
    def __controller(origin, target, size):
        sx, sy = origin
        ex, ey = target
        angle = pi + atan2(sy - ey, sx - ex)
        return ConstantController(size * cos(angle), size * sin(angle))

    def __init__(self, origin, target, size=8):
        """Initialize the object."""
        Collider.__init__(self, Collider.LINE)
        Controllable.__init__(self, Shot.__controller(origin, target, size))
        Movable.__init__(self, origin)
        Hideable.__init__(self)
        GameObject.__init__(self, GameObject.Priority.PROJECTILE)

        self.__next = None

    def update(self, bounds):
        """Update object."""
        self.__next = self.position
        self.move(*next(self.controller))
        x, _ = self.position
        _, _, w, _ = bounds
        if x > w:
            self.hide()

    def draw(self, screen):
        """Draw object on screen."""
        white = (255, 255, 255)
        x, y = self.position
        if self.__next:
            pygame.draw.line(screen, white, self.position, self.__next)

    def collide_with(self, object):
        """Act on object collision."""
        self.hide()

    @property
    def bounds(self):
        """Return the position and end of the line segment."""
        xo, yo = self.position
        xt, yt = self.__next if self.__next else (xo, yo)
        return (xo, yo, xt, yt)
