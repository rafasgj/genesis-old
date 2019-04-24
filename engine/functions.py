"""Functions than can be used in game script."""

from .util import Command

import random


def RandomInt(*args):
    """Return a random int number between a and b."""
    return Command(random.randint, *args)


def Choice(*args):
    """Return a random element from the given list."""
    return Command(random.choice, args)


def Add(*args):
    """Return the sum of all arguments."""
    t = type(args[0])
    return sum(map(t, args), t())


def Sub(*args):
    """Return the sum of all arguments."""
    t = type(args[0])
    args = map(t, args)
    return sum(map(lambda x: -1 * x, args[1:]), args[0])
