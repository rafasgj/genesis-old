"""Implement behaviors for game objects."""


class Controllable:
    """A controlable object is one that ask for a next movement delta."""

    def __init__(self, controller):
        """Initialize the controlable object with a control."""
        self.__controller = controller

    def update(self):
        """Update the object based on its controller."""
        self.movement = self.__controller.next_move()

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
