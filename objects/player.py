"""Define the player class."""

from engine.gameobject import GameObject
from engine.collider import Collider
from engine.behaviors import Controllable, Hideable, Movable
from engine.controllers import ConstantController
from engine.sprite import Sprite


class Player(Collider, Controllable, Hideable, Movable, GameObject):
    """Models the player objec."""

    def __init__(self, position, controller=ConstantController(0, 0)):
        """Initialize the object."""
        Collider.__init__(self, Collider.RECT)
        Controllable.__init__(self, controller)
        Hideable.__init__(self)
        Movable.__init__(self, position)
        GameObject.__init__(self, GameObject.Priority.PLAYER)
        self.__sprite = Sprite('media/images/f18.png', position)
        self.__lifes = 3
        self.__points = 0
        self.__speed = 5
        self.__move = (0, 0)

    def collide_with(self, object):
        """Enemy wal killed."""
        print(object)
        self.__lifes -= 1
        self.hide()

    def update(self, bounds):
        """Update object position."""
        if self.visible:
            try:
                self.move(*next(self.controller))
                self.offlimits(bounds)
            except Exception as e:
                pass

    def draw(self, screen):
        """Draw enemy on the screen."""
        if self.visible:
            self.__sprite.draw(screen, self.position)

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
