"""Define a scene (stage) for the game."""

from .gameobject import GameObject
from .collider import Collider
from .audio import Mixer
from .behaviors import NonRemovable
from .functions import SceneFunction

import importlib


def _find(data, item, default):
    path = item.split('.')
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


class SceneObject:
    """A scene object that must be loaded when needed."""

    def __init__(self, name):
        """Initialize object."""
        self.__name = name

    def __call__(self):
        """Get contained object string."""
        return self.__name


class SceneBehavior:
    """A scene behavior that must be loaded when needed."""

    def __init__(self, name):
        """Initialize object."""
        self.__name = name

    def __call__(self):
        """Get contained object string."""
        return self.__name


class Scene:
    """Models a game scene."""

    def __init__(self, game, config):
        """Initialize the Scene objects."""
        self.name = config['name']
        self.__object_configuration = {}
        self.__game_objects = []
        self.__events = []
        self.__keys = set()
        self.game = game
        self.mixer = Mixer(_find(config, 'mixer.config', {}))
        # configure audio
        for name, filename in _find(config, 'mixer.loops', {}).items():
            self.mixer.add(name, filename)
        # scene object descriptions
        for name, desc in config['objects'].items():
            self.__object_configuration[name] = desc
        # next scenes
        self.__next_scene = config.get('next_scene', {})
        # create events (when, recurrence, event, *args, **kwargs)
        self.__events = [(-1, 0, *e) for e in config.get('before', [])]
        self.__events.extend([e for e in config.get('events', [])])
        self.stop = False
        self.key_events = config.get('on_key', set())
        self.__behaviors = config.get('behaviors', set())
        self.__frame = 0
        self.__time = 0

    def __get_class(self, obj_class):
        module, classname = obj_class.rsplit('.', 1)
        return getattr(importlib.import_module(module), classname)

    def __load_object(self, description, **kwargs):
        def bind_key_event(k, fn, which):
            if isinstance(fn, str):
                fn = getattr(obj, fn)
            self.__keys.add(k)
            which(k, fn)

        def process_scene_parameter(param):
            if isinstance(param, SceneFunction):
                return process_scene_parameter(param())
            elif isinstance(param, SceneObject):
                return self.get_object(process_scene_parameter(param()))
            elif isinstance(param, SceneBehavior):
                behavior = self.__behaviors[process_scene_parameter(param())]
                return self.__load_object(behavior)
            else:
                return param

        cls = self.__get_class(description['class'])
        params = kwargs.get('init', description.get('init', {})).copy()
        for k, v in params.items():
            if isinstance(v, dict):
                params[k] = self.__load_object(v)
            elif isinstance(v, (SceneFunction, SceneObject, SceneBehavior)):
                params[k] = process_scene_parameter(v)
        try:
            obj = cls(**params)
        except Exception as e:
            print("Error intsantiating '{class}'".format(**description))
            raise
        for m, d, fn in description.get('notification', []):
            meth = getattr(obj, m)
            setattr(obj, m, d(fn, obj, self)(meth))
        events = description.get('bind', {})
        for k, fn in events.get('up', {}).items():
            bind_key_event(k, fn, self.game.on_key_up)
        for k, fn in events.get('down', {}).items():
            bind_key_event(k, fn, self.game.on_key_down)
        return obj

    def verify_collisions(self):
        """Verify collision in scene objects."""
        for i, (_, src) in enumerate(self.__game_objects):
            if isinstance(src, Collider) and src.should_collide:
                for (_, obj) in self.__game_objects[i + 1:]:
                    if isinstance(obj, Collider) and obj.should_collide:
                        if src.did_collide(obj):
                            src.collide_with(obj)
                            obj.collide_with(src)

    def get_object_list(self, name):
        """Retrieve a list of objects with the same name."""
        return [o for (n, o) in self.__game_objects if n == name]

    def get_object(self, name):
        """Retrieve an object or object description."""
        ol = self.get_object_list(name)
        if len(ol) == 0:
            error = "Object '{}' not found."
            raise Exception(error.format(name))
        if len(ol) > 1:
            error = "Requested one object, found many: {}"
            raise Exception(error.format(name))
        return ol[0]

    def update_objects(self, bounds):
        """Update game objects within bounds."""
        for (_, object) in self.__game_objects:
            object.update(bounds)
        self.__game_objects = [(n, o) for (n, o) in self.__game_objects
                               if isinstance(o, NonRemovable) or
                               not hasattr(o, 'visible') or o.visible]

    def draw(self, window):
        """Draw scene on window."""
        for (_, object) in list_reverse(self.__game_objects):
            window.draw(object)

    def frame(self, count, elapsed):
        """Handle new frame event."""
        self.__frame = count
        self.__time += elapsed
        self.__events.sort(key=lambda e: int(e[0]))
        for i, (t, n, *e) in enumerate(self.__events):
            t -= elapsed
            if t <= 0:
                self.event(*e)
                t = n
            self.__events[i] = (t, n, *e)
        self.__events = [(t, *e) for t, *e in self.__events if t > 0]

    def queue_event(self, time, repeat, event, *args):
        """Queue an event to the scene."""
        self.__events.append((time, repeat, event, *args))

    def event(self, func, *args, **kwargs):
        """Execute a scene event."""
        fn = getattr(type(self), "_" + func)
        fn(self, *args, **kwargs)

    # Events that can be executed in scene scripts
    def _spawn(self, objects, **kwargs):
        def add_object(obj_name):
            # add object
            obj_desc = self.__object_configuration[obj_name]
            if isinstance(obj_desc, GameObject):
                self.__game_objects.append((obj_name, obj_desc))
            else:
                obj = self.__load_object(obj_desc, **kwargs)
                self.__game_objects.append((obj_name, obj))
        if isinstance(objects, str):
            add_object(objects)
        else:
            for object_name in objects:
                add_object(object_name)
        self.__game_objects.sort(key=lambda go: go[1].priority)

    def _music_start(self, music):
        self.mixer.play_loop(music)

    def _play(self, sound):
        self.mixer.play(sound)

    def _object(self, name, method, *args, **kwargs):
        obj = self.get_object(name)
        fn = getattr(type(obj), method)
        fn(obj, *args, **kwargs)

    def _call(self, callable, *args, **kwargs):
        callable(self, *args, **kwargs)

    def _end_scene(self, *args, **kwargs):
        """End scene for the script."""
        self.end_scene(*args, **kwargs)

    def end_scene(self, *args, **kwargs):
        """End scene for the script."""
        for (key, *_) in self.key_events | self.__keys:
            self.game.remove_key(key)
        self.stop = True
        self.mixer.stop()

    def _game_over(self):
        self.game.game_over()

    @property
    def next_scene(self):
        """Query the next scenes."""
        return self.__next_scene

    @property
    def elapsed(self):
        """Query the number of frames executed and the elapsed time."""
        return (self.__frame, self.__time)
