"""The base game class."""

import pygame
from .gameobject import GameObject
from .collider import Collider
from .audio import Mixer
from collections import defaultdict

import importlib
from functools import partial


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


class Scene:
    """Models a game scene."""

    def __init__(self, config):
        """Initialize the Scene objects."""
        self.__object_configuration = {}
        self.__game_objects = []
        self.__events = []
        self.mixer = Mixer(_find(config, 'mixer.config', {}))
        # disable key responders
        # for dk in script.get("disable_keys", []):
        #     self.remove_key(**dk)
        # configure audio
        for name, filename in _find(config, 'mixer.loops', {}).items():
            self.mixer.add(name, filename)
        # scene object descriptions
        for name, desc in config['objects'].items():
            self.__object_configuration[name] = desc
        # create events (when, recurrence, event, *args, **kwargs)
        self.__events = [(-1, 0, *e) for e in config.get('before', [])]
        self.__events.extend([e for e in config.get('events', [])])
        self.__events.sort(key=lambda e: int(e[0]))
        self.stop = False
        self.next_scene = config.get('next_scene', None)
        self.key_events = config.get('on_key', [])

    def __get_class(self, obj_class):
        module, classname = obj_class.rsplit('.', 1)
        return getattr(importlib.import_module(module), classname)

    def __load_object(self, description, **kwargs):
        cls = self.__get_class(description['class'])
        params = kwargs.get('init', description.get('init', {}))
        for k, v in params.items():
            if isinstance(v, dict):
                params[k] = self.__load_object(v)
        return cls(**params)

    def verify_collisions(self):
        """Verify collision in scene objects."""
        for i, src in enumerate(self.__game_objects):
            if isinstance(src, Collider) and src.should_collide:
                for obj in self.__game_objects[i + 1:]:
                    if isinstance(obj, Collider) and obj.should_collide:
                        if src.did_collide(obj):
                            src.collide_with(obj)
                            obj.collide_with(src)

    def get_object(self, name):
        """Retrieve an object or object description."""
        return self.__object_configuration.get(name, None)

    def update_objects(self, bounds):
        """Update game objects within bounds."""
        for object in self.__game_objects:
            object.update(bounds)
        self.__game_objects = [o for o in self.__game_objects
                               if not hasattr(o, 'visible') or o.visible]

    def draw(self, window):
        """Draw scene on window."""
        for object in list_reverse(self.__game_objects):
            window.draw(object)

    def frame(self, count, elapsed):
        """Handle new frame event."""
        for i, (t, n, *e) in enumerate(self.__events):
            t -= elapsed
            if t <= 0:
                self.event(*e)
                t = n
            self.__events[i] = (t, n, *e)
        self.__events = [(t, *e) for t, *e in self.__events if t > 0]
        self.__events.sort(key=lambda e: int(e[0]))

    def event(self, func, *args, **kwargs):
        """Execute a scene event."""
        fn = getattr(type(self), "_" + func)
        fn(self, *args, **kwargs)

    # Events that can be executed in scene scripts
    def _spawn(self, object_name, **kwargs):
        obj_desc = self.__object_configuration[object_name]
        # add object
        if isinstance(obj_desc, GameObject):
            self.__game_objects.append(obj_desc)
        else:
            self.__game_objects.append(self.__load_object(obj_desc, **kwargs))
        self.__game_objects.sort(key=lambda go: go.priority)

    def _music_start(self, music):
        self.mixer.play_loop(music)

    def _play(self, sound):
        self.mixer.play(sound)

    def _object(self, name, method, *args, **kwargs):
        obj = self.get_object(name)
        fn = getattr(type(obj), method)
        fn(obj, *args, **kwargs)

    def end_scene(self, *args, **kwargs):
        """Tell scene to end."""
        self.stop = True


class Game:
    """The base game class."""

    @classmethod
    def __ignore_event(*args, **kwargs):
        pass

    def __init__(self, **kwargs):
        """
        Initialize the game object.

        Optional name parameters:
            - fps: the maximum number of fames per second. (Default: 60)
        """
        self.running = False
        self.__clock = pygame.time.Clock()
        self.__fps = kwargs.get('fps', 60)
        self.__scenes = []
        self.__events = {
            pygame.QUIT: self.stop,
            pygame.KEYDOWN: self.__keydown,
            pygame.KEYUP: self.__keyup,
        }
        self.__registered_timers = defaultdict(set)
        # Scene configurable stuff.
        self.__game_objects = []
        self.__keymap = defaultdict(set)
        self.__keymap[pygame.K_ESCAPE].add(self.stop)
        self.__current_scene = None

    def stop(self, *args, **kwargs):
        """Stop running the game."""
        self.running = False

    def __keydown(self, event):
        """Handle keyboard press events."""
        if event.key != pygame.K_ESCAPE:
            mapped = self.__keymap[event.key].copy()
            for fn in mapped:
                fn(event, self.__current_scene)

    def __keyup(self, event):
        """Handle keyboard release events."""
        mapped = self.__keymap[event.key].copy()
        for fn in mapped:
            fn(event, self.__current_scene)

    def add_timer(self, responder, interval):
        """Register a timer."""
        if not hasattr(Game.add_timer, 'event'):
            event = pygame.USEREVENT
        else:
            event = self.add_timer.event + 1
        Game.add_timer.event = event
        self.__events[event] = responder
        pygame.time.set_timer(event, interval)
        return event

    def remove_timer(self, event):
        """Remove a timer."""
        del(self.__events[event])

    def __start_scene(self, script):
        if self.__current_scene:
            for key, handler in self.__current_scene.key_events:
                self.remove_key(key, handler)
        scene = Scene(script)
        for key, handler in scene.key_events:
            fn = partial(getattr(scene, handler), self)
            self.on_key(key, fn)
        return scene

    def run(self, script):
        """Start the game loop."""
        self.running = True
        frame = 0
        self.__current_scene = self.__start_scene(script)
        while self.running and self.__current_scene:
            # notify scene of new frame.
            self.__current_scene.frame(frame, 1000 / self.__fps)
            frame += 1
            # handle events
            for event in pygame.event.get():
                self.__events.get(event.type, Game.__ignore_event)(event)
            # verify collisions
            self.__current_scene.verify_collisions()
            # update objects
            self.__current_scene.update_objects(self.__window.bounds)
            # draw objects
            self.__window.clear()
            self.__current_scene.draw(self.__window)
            # swap buffers
            pygame.display.update()
            # ensure loop do not run faster than FPS.
            self.__clock.tick(self.__fps)
            if self.__current_scene.stop:
                self.__current_scene = \
                    self.__start_scene(self.__current_scene.next_scene)

    def on_key(self, keys, responder):
        """Define a responder for a keyboard event."""
        # we'll save ESCAPE to always quit the game, useful on fullscreen...
        try:
            for k in keys:
                if k != pygame.K_ESCAPE:
                    self.__keymap[k].add(responder)
        except TypeError as _:
            if keys != pygame.K_ESCAPE:
                self.__keymap[keys].add(responder)
        return self

    def remove_key(self, keys, responder):
        """Define a responder for a keyboard event."""
        # we'll save ESCAPE to always quit the game, useful on fullscreen...
        try:
            for k in keys:
                if k != pygame.K_ESCAPE:
                    if responder in self.__keymap[k]:
                        self.__keymap[k].remove(responder)
        except TypeError as _:
            if keys != pygame.K_ESCAPE:
                if responder in self.__keymap[keys]:
                    self.__keymap[keys].remove(responder)
        return self

    @property
    def window(self):
        """Retrieve the game window"""
        return self.__window

    @window.setter
    def window(self, w):
        """Set the game window, if not set. It is a write-only property."""
        if not hasattr(self, "__window"):
            self.__window = w
