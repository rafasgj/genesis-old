"""Define behaviors for killable objects."""

from engine import Hideable
from .explosion import Explosion


class Killable(Hideable):
    """Define a behavior for objects that could be killed."""

    def __init__(self, explosion_type, time_scale=1.0):
        """Initialize the object."""
        Hideable.__init__(self)
        self.__explosion = None
        self.__dying = False
        self.__type = explosion_type
        self.__time_scale = time_scale

    @property
    def should_update(self):
        """Check if object should be updated."""
        return self.visible and not self.__dying

    def update(self, bounds):
        """Update explosion."""
        if self.__dying:
            self.__explosion.update(bounds)
            if not self.__explosion.visible:
                self.hide()
                self.__dying = False

    def draw(self, screen):
        """Draw explosion."""
        if self.__dying:
            self.__explosion.draw(screen)

    def die(self):
        """Mark object to die."""
        self.__dying = True
        self.__explosion = Explosion(self.position, self.__type,
                                     time_scale=self.__time_scale)
