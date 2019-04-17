"""An asteroid that the player can crash into."""

from engine import (Sprite, GameObject, Collider, Controllable, Movable,
                    ConstantController)


class Asteroid(Collider, Controllable, Movable, GameObject):
    """Model an asteroid game object."""

    def __init__(self, pos, scale=1, **kw):
        """Initialize the game object."""
        Collider.__init__(self, kw.get('shape', Collider.ELLIPSE))
        Controllable.__init__(self, ConstantController(-1, 0))
        Movable.__init__(self, pos)
        GameObject.__init__(self, GameObject.Priority.BOSS)
        self.__sprite = Sprite('media/images/asteroid.png',
                               scale=scale, rotate=0)

    def update(self, bounds):
        """Update object position."""
        try:
            self.move(*next(self.controller))
            self.offlimits(bounds)
        except Exception as e:
            pass

    def draw(self, screen):
        """Draw object on the screen."""
        self.__sprite.draw(screen, self.position)
        # pygame.draw.ellipse(screen, (255, 0, 255), self.__sprite.bounds, 2)

    def offlimits(self, limits):
        """Take action when object is off-limits, return if needs update."""
        wx, wy, ww, wh = limits
        x, y, w, h = self.bounds
        if x + w < wx:
            self.hide()

    def collide_with(self, object):
        """Asteroids are imune to collision."""
        pass

    @property
    def bounds(self):
        """Query object bounds."""
        x, y = self.position
        _, _, rx, ry = list(map(lambda n: n // 2, self.__sprite.bounds))
        return (x + rx, y + ry, rx, ry)
