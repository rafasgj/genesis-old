"""Utility functions."""


class Command:
    """Store a command for later execution."""

    def __init__(self, command, *args, **kwargs):
        """Initialize the object."""
        self.__comm = command
        self.__args = args
        self.__kwargs = kwargs

    def __call__(self, *args, **kwargs):
        """Execute the stored command."""
        return self.__comm(*self.__args, **self.__kwargs)


class TheGame:
    """Store an instance of the running game."""

    def __call__(self):
        """Return the instance of the running game."""
        return TheGame.game


def get_value(data, path, default=None):
    """Find a value in a dict using dot-notation for path."""
    path = path.split('.')
    if not path[0] in data:
        return default
    d = data[path[0]]
    for i in path[1:]:
        if i not in d:
            return default
        d = d[i]
    return d


def list_reverse(lst):
    """Get elements of a list in reverse order."""
    c = len(lst)
    while c > 0:
        c -= 1
        yield lst[c]
    raise StopIteration


class ValueReference(object):
    """Reference some data to be retrieved later."""

    def __init__(self, value):
        """Initialize object."""
        object.__init__(self)
        self.__value = value

    def __call__(self):
        """Get contained object string."""
        return self.__value


class PropertyReference(object):
    """Referece the value of a property object to be accessed later."""

    def __init__(self, object, property):
        """Initialize the property object."""
        self.__name = object
        self.__property = property

    def __int__(self):
        """Convert to int."""
        return int(self.value)

    def __str__(self):
        """Convert to str."""
        value = self.value
        return str(value)

    def __iter__(self):
        """Treat property as an iterator."""
        value = self.value
        if not isinstance(value, (tuple, list)):
            raise Exception("Property is not iterable.")
        self.__iter_count = 0
        return self

    def __next__(self):
        """Retrieve the next element."""
        value = self.value
        if isinstance(value, (tuple, list)):
            if self.__iter_count < len(value):
                self.__iter_count += 1
                return value[self.__iter_count - 1]
        raise StopIteration

    @property
    def value(self):
        """Return the value of the property."""
        # TODO: Fix this reference...
        scene = TheGame()().current_scene
        obj = scene.get_object(self.__name)
        return getattr(obj, self.__property)
