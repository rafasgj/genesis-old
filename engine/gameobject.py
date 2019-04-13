"""Basic attributes and behavior of game objects."""

from enum import Enum


class GameObject:
    """Define the basic attributes and behavior of all game objects."""

    class Priority(Enum):
        """Priorities for game objects."""

        PROJECTILE = 0
        PLAYER = 1
        NPC = 10
        BOSS = 20
        DEFAULT = 500
        BACKGROUND = 1000

    def __init__(self, priority: Priority):
        """Initialize the common Game Object data."""
        self.__priority = priority.value

    def update(self):
        """Update the object state."""
        raise NotImplementedError("Method update() is not implemented.")

    def draw(self, screen):
        """Draw object on the screen."""
        raise NotImplementedError("Method update() is not implemented.")

    @property
    def priority(self):
        """Return the object priority."""
        return self.__priority
