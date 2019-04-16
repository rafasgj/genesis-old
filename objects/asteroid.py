"""An asteroid that the player can crash into."""

from engine.sprite import Sprite
from engine.gameobject import GameObject
from engine.collider import Collider
from engine.behaviors import Controllable, Movable
from engine.controllers import ConstantController


class Asteroid(Collider, Controllable, Movable, GameObject):
    """Model an asteroid game object."""

    def __init__(self, pos, scale=1, **kw):
        """Initialize the game object."""
        Collider.__init__(self, kw.get('shape', Collider.ELLIPSE))
        Controllable.__init__(self, ConstantController(-2, 0))
        Movable.__init__(self, pos)
        GameObject.__init__(self, GameObject.Priority.BOSS)
        self.__sprite = Sprite('media/images/asteroid.png',
                               scale=scale, rotate=0)

    def update(self, bounds):
        """Update object position."""
        try:
            self.move(*next(self.controller))
        except Exception as e:
            pass

    def draw(self, screen):
        """Draw object on the screen."""
        self.__sprite.draw(screen, self.position)
        # pygame.draw.ellipse(screen, (255, 0, 255), self.__sprite.bounds, 2)

    def offlimits(self, limits):
        """Take action when object is off-limits, return if needs update."""
        h, v = limits
        if True in limits:
            if h:
                self.hide()
            return False
        return True

    def collide_with(self, object):
        """Asteroids are imune to collision."""
        pass

    @property
    def bounds(self):
        """Query object bounds."""
        x, y = self.position
        _, _, rx, ry = list(map(lambda n: n // 2, self.__sprite.bounds))
        return (x + rx, y + ry, rx, ry)
