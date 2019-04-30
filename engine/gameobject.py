"""Basic attributes and behavior of game objects."""

from .util import Bindable

from enum import Enum


class GameObject(Bindable):
    """Define the basic attributes and behavior of all game objects."""

    class Priority(Enum):
        """Priorities for game objects."""

        UI = 0
        PROJECTILE = 5
        PLAYER = 10
        NPC = 20
        BOSS = 50
        DEFAULT = 500
        BACKGROUND = 1000

    def __init__(self, priority):
        """Initialize the common Game Object data."""
        Bindable.__init__(self)
        self.__priority = priority.value \
            if isinstance(priority, Enum) else priority
        self.__valid = True

    def update(self, bounds):
        """Update the object state."""
        raise NotImplementedError("Method update() is not implemented.")

    def draw(self, screen):
        """Draw object on the screen."""
        raise NotImplementedError("Method draw() is not implemented.")

    def offlimits(self, limits):
        """Take action when object is off-limits, return if needs update."""
        raise NotImplementedError("Method offlimits() is not implemented.")

    @property
    def priority(self):
        """Return the object priority."""
        return self.__priority

    @property
    def can_eliminate(self):
        """Query if the object can be eliminated."""
        return not self.__valid

    def destroy(self):
        """Mark the object for elimination."""
        self.__valid = False
