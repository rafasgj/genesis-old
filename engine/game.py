"""The base game class."""

from .scene import Scene
from .util import get_value, list_reverse
from .window import Window
from .util import ValueReference, TheGame, GameVariable
from .text import Font

import pygame

from collections import defaultdict
from functools import partial


class GameFont(ValueReference):
    """Provide the name of a game font."""

    pass


class Game:
    """The base game class."""

    @classmethod
    def __ignore_event(*args, **kwargs):
        pass

    def __load_fonts(self, fonts):
        result = {}
        for name, config in fonts.items():
            filename = config['filename']
            for id, size in config['sizes'].items():
                f = Font(filename, size)
                result["{}.{}".format(name, id)] = f
        return result

    def __init_window(self, config):
        modes = sorted(pygame.display.list_modes())
        minimum = config.get("minimum", modes[0])
        maximum = config.get("maximum", modes[-1])
        size = config.get("size", "maximum")
        if size == "maximum":
            for mode in list_reverse(modes):
                if mode <= maximum:
                    size = mode
                    break
        elif size == "minimum":
            for mode in modes:
                if mode >= minimum:
                    size = mode
                    break
        fullscreen = config.get("fullscreen", False)
        return Window(size=size, fullscreen=fullscreen)

    def __init__(self, script, **kwargs):
        """
        Initialize the game object.

        Optional name parameters:
            - fps: the maximum number of fames per second. (Default: 60)
        """
        self.running = False
        self.__clock = pygame.time.Clock()
        self.__fps = get_value(script, 'fps', 60)
        self.__scenes = {}
        self.__events = {
            pygame.QUIT: self.stop,
            pygame.KEYDOWN: self.__keydown,
            pygame.KEYUP: self.__keyup,
        }
        self.__registered_timers = defaultdict(set)
        # Scene configurable stuff.
        self.__keydown = {}
        self.__keyup = {}
        self.__keyup.update({pygame.K_ESCAPE: self.stop})
        self.__current_scene = None
        self.__game_over = True
        self.__fonts = self.__load_fonts(script.get("fonts", {}))
        self.__window = self.__init_window(script['window'])
        self.__variables = {name: GameVariable(name, desc, self) for name, desc
                            in script.get("variables", {}).items()}
        TheGame.game = self

    def bind_variables(self, cls, obj):
        """Bind variable notifications to objects of a class."""
        for n, v in self.__variables.items():
            v.bind_notifications(cls, obj)

    def get_variable(self, name):
        """Retrieve a Game Variable."""
        return self.__variables[name]

    def get_font(self, fontsize):
        """Get font object."""
        return self.__fonts[fontsize]

    def stop(self, *args, **kwargs):
        """Stop running the game."""
        self.running = False

    def __keydown(self, event):
        """Handle keyboard press events."""
        if event.key != pygame.K_ESCAPE:
            fn = self.__keydown.get(event.key, Game.__ignore_event)
            fn(event, self.__current_scene)

    def __keyup(self, event):
        """Handle keyboard release events."""
        fn = self.__keyup.get(event.key, Game.__ignore_event)
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
        self.__game_over = False
        if script is None:
            self.running = False
            return None
        scene = Scene(self, script)
        for (key, handler) in scene.key_events:
            fn = partial(getattr(scene, handler), self)
            self.on_key_up(key, fn)
        self.__current_scene = scene

    def run(self, first_scene):
        """Start the game loop."""
        self.running = True
        frame = 0
        self.__start_scene(self.__scenes[first_scene])
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
                next = "game_over" if self.__game_over else "end_scene"
                scenes = self.__current_scene.next_scene
                scene = scenes[next]
                self.__start_scene(self.__scenes[scene])
                frame = 0

    def add_scene(self, scene):
        """Add a scene to the script."""
        self.__scenes[scene['name']] = scene

    def __register_key_event(self, keys, responder, event_list):
        try:
            for k in keys:
                if k != pygame.K_ESCAPE:
                    event_list[k] = responder
        except TypeError as _:
            if keys != pygame.K_ESCAPE:
                event_list[keys] = responder

    def on_key_down(self, keys, responder):
        """Define a responder for a keyboard event."""
        # we'll save ESCAPE to always quit the game, useful on fullscreen...
        self.__register_key_event(keys, responder, self.__keydown)
        return self

    def on_key_up(self, keys, responder):
        """Define a responder for a keyboard event."""
        # we'll save ESCAPE to always quit the game, useful on fullscreen...
        self.__register_key_event(keys, responder, self.__keyup)
        return self

    def remove_key(self, keys):
        """Define a responder for a keyboard event."""
        def remove_event(key):
            if key != pygame.K_ESCAPE:
                if key in self.__keydown:
                    del(self.__keydown[key])
                if key in self.__keyup:
                    del(self.__keyup[key])
        # we'll save ESCAPE to always quit the game, useful on fullscreen...
        try:
            for k in keys:
                remove_event(k)
        except TypeError as _:
            remove_event(keys)
        return self

    def get_object(self, object):
        """Retrieve an object from the game or the current scene."""
        if object in self.__variables:
            return self.__variables[object]
        return self.__current_scene.get_object(object)

    def game_over(self):
        """Mark the game as game over."""
        self.__game_over = True
        self.__current_scene.end_scene()

    @property
    def window(self):
        """Retrieve the game window"""
        return self.__window

    @property
    def current_scene(self):
        """Retrieve current running scene."""
        return self.__current_scene
