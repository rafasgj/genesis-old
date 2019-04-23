"""Functions than can be used in game script."""

from random import randint, choice


class SceneFunction:
    """Base of all scene functions."""

    pass


class RandomInt(SceneFunction):
    """Return an Integer in the range [a..b]."""

    def __init__(self, a, b):
        """Initialize object."""
        self.__a = a
        self.__b = b

    def __call__(self):
        """Execute object."""
        return randint(self.__a, self.__b)


class Choice(SceneFunction):
    """Return one of several options."""

    def __init__(self, *args):
        """Initialize object."""
        self.__options = args

    def __call__(self):
        """Execute object."""
        return choice(self.__options)
