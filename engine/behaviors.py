"""Implement behaviors for game objects."""

import operator


class Controllable:
    """A controlable object is one that ask for a next movement delta."""

    def __init__(self, controller):
        """Initialize the controlable object with a control."""
        self.__controller = controller

    # Automate controller movement.

    @property
    def controller(self):
        """Retrieve the object controller function."""
        return self.__controller


class Hideable:
    """Define behavior to hide object."""

    def __init__(self):
        """Initialize the Hideable part of the object."""
        self.__visible = True

    @property
    def visible(self):
        """Verify if object is visible."""
        return self.__visible

    def hide(self):
        """Hide the object."""
        self.__visible = False


class Movable:
    """Define a movable object."""

    def __init__(self, position):
        """Initialize the object."""
        self.__position = position

    @property
    def position(self):
        """Return the current position."""
        return self.__position

    def move(self, dx, dy):
        """Move object."""
        self.__position = tuple(map(operator.add, self.position, (dx, dy)))
