"""Basic attributes and behavior of game objects."""


class GameObject:
    """Define the basic attributes and behavior of all game objects."""

    def __init__(self, priority):
        """Initialize the common Game Object data."""
        self.__priority = priority

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
