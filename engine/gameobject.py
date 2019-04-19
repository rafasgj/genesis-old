"""Basic attributes and behavior of game objects."""

from enum import Enum


class GameObject:
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
        self.__priority = priority.value \
            if isinstance(priority, Enum) else priority

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
