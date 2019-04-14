"""An asteroid that the player can crash into."""

from engine.sprite import Sprite
import pygame
from engine.gameobject import GameObject
from engine.collider import Collider
from engine.behaviors import Controllable
from engine.controllers import ConstantController


class Asteroid(Collider, Controllable, GameObject):
    """Model an asteroid game object."""

    def __init__(self, pos, scale=1, **kw):
        """Initialize the game object."""
        Collider.__init__(self, kw.get('shape', Collider.ELLIPSE))
        Controllable.__init__(self, ConstantController(-2, 0))
        GameObject.__init__(self, GameObject.Priority.BOSS)
        self.__sprite = Sprite('media/images/asteroid.png', pos,
                               scale=scale, rotate=0)

    def update(self):
        """Update object position."""
        try:
            dx, dy = next(self.controller)
            self.__sprite.move = (dx, dy)
        except Exception as e:
            self.__sprite.move = (0, 0)
        self.__sprite.update()

    def draw(self, screen):
        """Draw object on the screen."""
        self.__sprite.draw(screen)
        # pygame.draw.ellipse(screen, (255, 0, 255), self.__sprite.bounds, 2)

    def collide_with(self, object):
        """Asteroids are imune to collision."""
        pass

    @property
    def bounds(self):
        """Query object bounds."""
        x, y, rx, ry = self.__sprite.bounds
        rx //= 2
        ry //= 2
        return (x + rx, y + ry, rx, ry)
