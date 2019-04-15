"""Define the player class."""

from engine.gameobject import GameObject
from engine.collider import Collider
from engine.behaviors import Controllable, Hideable
from engine.controllers import ConstantController
from engine.sprite import Sprite


class Player(Collider, Controllable, Hideable, GameObject):
    """Models the player objec."""

    def __init__(self, position, controller=ConstantController(0, 0)):
        """Initialize the object."""
        Collider.__init__(self, Collider.RECT)
        Controllable.__init__(self, controller)
        Hideable.__init__(self)
        GameObject.__init__(self, GameObject.Priority.PLAYER)
        self.__lifes = 3
        self.__points = 0
        self.__speed = 5
        self.__sprite = Sprite('media/images/f18.png', position)

    def collide_with(self, object):
        """Enemy wal killed."""
        self.__lifes -= 1
        self.hide()

    def update(self):
        """Update object position."""
        if self.visible:
            try:
                dx, dy = next(self.controller)
                self.__sprite.move = (dx * self.__speed, dy * self.__speed)
            except Exception as e:
                self.__sprite.move = (0, 0)
            self.__sprite.update()

    def draw(self, screen):
        """Draw enemy on the screen."""
        if self.visible:
            self.__sprite.draw(screen)

    def add_points(self, points):
        """Add points to player."""
        if points > 0:
            self.__points += points

    def accelerate(self):
        """Make the player faster."""
        if self.__speed < 7.5:
            self.__speed += 0.5

    @property
    def lives(self):
        """Query player lives."""
        return self.__lives

    @property
    def points(self):
        """Query player lives."""
        return self.__points

    @property
    def bounds(self):
        """Query object bounds."""
        return self.__sprite.bounds
