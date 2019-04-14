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
