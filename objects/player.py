"""Define the player class."""

from engine import (GameObject, Collider, Controllable, Movable,
                    ConstantController, Sprite, NonRemovable)
from .killable import Killable
from .explosion import Explosion
from .projectile import Projectile


class Player(Collider, Controllable, Movable, Killable, GameObject,
             NonRemovable):
    """Models the player objec."""

    def __init__(self, position, speed=5, controller=ConstantController(0, 0)):
        """Initialize the object."""
        Collider.__init__(self, Collider.RECT)
        Controllable.__init__(self, controller)
        Movable.__init__(self, position)
        Killable.__init__(self, Explosion.BIG)
        GameObject.__init__(self, GameObject.Priority.PLAYER)
        self.__original_position = position
        self.__sprite = Sprite('media/images/f18.png')
        self.__lives = 3
        self.__points = 0
        self.__speed = speed
        self.__move = (0, 0)

    def collide_with(self, object):
        """Enemy wal killed."""
        if isinstance(object, Projectile) and \
           isinstance(self, object.creator):
            return
        if self.should_update:
            self.__lives -= 1
            self.should_collide = False
            self.die()

    def update(self, bounds):
        """Update object position."""
        if self.should_update:
            try:
                mv = next(self.controller)
                self.move(*list(map(lambda n: self.__speed * n, mv)))
                self.offlimits(bounds)
            except StopIteration as si:
                pass
        else:
            Killable.update(self, bounds)

    def draw(self, screen):
        """Draw enemy on the screen."""
        if self.should_update:
            self.__sprite.draw(screen, self.position)
        else:
            Killable.draw(self, screen)

    def add_points(self, points):
        """Add points to player."""
        if points > 0:
            self.__points += points

    def accelerate(self):
        """Make the player faster."""
        if self.__speed < 7.5:
            self.__speed += 0.5

    def offlimits(self, limits):
        """Take action when object is off-limits, return if needs update."""
        wx, wy, ww, wh = limits
        x, y, w, h = self.bounds
        dx = wx if x < wx else x
        dx = (wx + ww) - w if (x + w) > (wx + ww) else dx
        dx -= x
        dy = wy if y < wy else y
        dy = (wy + wh) - h if (y + h) > (wy + wh) else dy
        dy -= y
        self.move(dx, dy)

    def respawn(self):
        """Respawn player."""
        x, y = self.position
        ox, oy = self.__original_position
        self.move(ox - x, oy - y)
        self.should_collide = True
        self.show()
        Killable.respawn(self)

    @property
    def bounds(self):
        """Query object bounds."""
        x, y = self.position
        _, _, w, h = self.__sprite.bounds
        return (x, y, w, h)

    @property
    def lives(self):
        """Query player lives."""
        return self.__lives

    @property
    def points(self):
        """Query player points."""
        return self.__points
