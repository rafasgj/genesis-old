"""Implement several utilities for dispatching notification of events."""

from collections import defaultdict


class Notifier:
    """Define a class that handles publish/subscribe events."""

    def __init__(self):
        """Initialize the notifier object."""
        self.__subscribers = defaultdict(set)

    def subscribe(self, notification, receiver):
        """Subscribe object receiver to a notification."""
        self.__subscribers[notification].add(receiver)

    def unsubscribe(self, notification, receiver):
        """Unsubscribe object receiver from a notification."""
        self.__subscribers[notification].remove(receiver)

    def notify(self, notification, *args, **kwargs):
        """Notify all listeners."""
        for listener in self.__subscribers[notification]:
            listener(*args, **kwargs)


class event_listener(object):
    """Decorator dispatched before methods are called."""

    __before = Notifier()
    __after = Notifier()

    def __init__(self, **argdict):
        """Initialize the notification wrapper."""
        self.__args = argdict.get('args', None)
        self.__kwargs = argdict.get('kwargs', None)
        self.__b = argdict.get('before', lambda *args, **kwargs: None)
        self.__a = argdict.get('after', lambda *args, **kwargs: None)

    def __call__(self, fn):
        """Call original function, decorated."""
        def wrapper(*args, **kwargs):
            event_listener.__before.notify(fn, *self.__args, **self.__kwargs)
            fn(*args, *kwargs)
            event_listener.__after.notify(fn, *self.__args, **self.__kwargs)

        event_listener.__before.subscribe(fn, self.__b)
        event_listener.__after.subscribe(fn, self.__a)
        return wrapper


def before(fn, *args, **kwargs):
    """Define a notification to be called before the callable."""
    return event_listener(before=fn, args=args, kwargs=kwargs)


def after(fn, *args, **kwargs):
    """Define a notification to be called after the callable."""
    return event_listener(after=fn, args=args, kwargs=kwargs)
