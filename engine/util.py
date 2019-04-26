"""Utility functions."""

from util.notifications import after, before


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
        obj = TheGame()().get_object(self.__name)
        if obj is None:
            obj = TheGame()().get_variable(self.__name)
        return getattr(obj, self.__property)


class Bindable(object):
    """Define an object that can bind to other object notifications."""

    def __init__(self, bindings=[]):
        """Initialize Bindable part of the object."""
        self.__bindings = bindings

    def bindings(self, bindings):
        """Set object bindings."""
        self.__bindings = bindings

    def bind_notifications(self, cls, obj):
        """Bind all notifications."""
        binders = {
            "after": after,
            "before": before
        }
        for n, c, m, h, *p in self.__bindings:
            if c == cls:
                binder = binders[n]
                meth = getattr(obj, m)
                handler = getattr(self, h)
                setattr(obj, m, binder(handler, *p)(meth))


class GameVariable(Bindable):
    """Models a Game (global) Variable."""

    def __init__(self, name, description=None, game=None):
        """Initialize object."""
        Bindable.__init__(self, description.get('bind', [])
                          if description is not None else [])
        self.__game = game
        self.__name = name
        self.__value = 0
        if description is not None:
            self.__value = description['value']
            self.__initial = self.__value

    def max(self, value):
        """Add a value to this variable."""
        self.__value = value if value > self.__value else self.__value

    def add(self, value):
        """Add a value to this variable."""
        self.__value += value

    def sub(self, value):
        """Subtract a value to this variable."""
        self.__value -= value

    def reset(self):
        """Reset variable to initial state."""
        self.__value = self.__initial

    @property
    def name(self):
        """Retrieve variable name."""
        return self.__name

    @property
    def value(self):
        """Retrieve variable value."""
        return self.__value

    def __str__(self):
        """Retrieve object value as a string."""
        return str(self.__value)

    def __int__(self):
        """Retrieve object value as an integer."""
        return int(self.__value)


class Self(object):
    """Represent the own object."""

    pass
