"""The base game class."""

import pygame
from .gameobject import GameObject
from .collider import Collider
from collections import defaultdict


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
        self.__game_objects = []
        self.__events = {
            pygame.QUIT: self.stop,
            pygame.KEYDOWN: self.__keydown,
            pygame.KEYUP: self.__keyup,
        }
        self.__keymap = defaultdict(set)
        self.__keymap[pygame.K_ESCAPE].add(self.stop)

    def stop(self, *args, **kwargs):
        """Stop running the game."""
        self.running = False

    def __keydown(self, event):
        """Handle keyboard press events."""
        if event.key != pygame.K_ESCAPE:
            for fn in self.__keymap[event.key]:
                fn(event)

    def __keyup(self, event):
        """Handle keyboard release events."""
        for fn in self.__keymap[event.key]:
            fn(event)

    def run(self):
        """Start the game loop."""
        def list_reverse(lst):
            c = len(lst)
            while c > 0:
                c -= 1
                yield lst[c]
            raise StopIteration

        self.running = True
        while self.running:
            # handle events
            for event in pygame.event.get():
                self.__events.get(event.type, Game.__ignore_event)(event)
            # verify collisions
            for i in range(len(self.__game_objects) - 1):
                src = self.__game_objects[i]
                if isinstance(src, Collider):
                    for obj in self.__game_objects[i + 1:]:
                        if isinstance(obj, Collider):
                            if src.did_collide(obj):
                                src.collide_with(obj)
                                obj.collide_with(src)
            # update objects
            for object in self.__game_objects:
                object.update()
            # draw objects
            self.__window.clear()
            for object in list_reverse(self.__game_objects):
                self.__window.draw(object)
            # swap buffers
            pygame.display.update()
            # ensure loop do not run faster than FPS.
            self.__clock.tick(self.__fps)

    def on_key(self, key, responder):
        """Define a responder for a keyboard event."""
        # we'll save ESCAPE to always quit the game, useful on fullscreen...
        if isinstance(type(key), type(pygame.K_ESCAPE)):
            if key == pygame.K_ESCAPE:
                return
            self.__keymap[key].add(responder)
        else:
            if pygame.K_ESCAPE in key:
                return
            for k in key:
                self.__keymap[k].add(responder)
        return self

    def remove_key(self, key, responder):
        """Define a responder for a keyboard event."""
        # we'll save ESCAPE to always quit the game, useful on fullscreen...
        if isinstance(type(key), type(pygame.K_ESCAPE)):
            if key == pygame.K_ESCAPE:
                return
            self.__keymap[key].remove(responder)
        else:
            if pygame.K_ESCAPE in key:
                return
            for k in key:
                self.__keymap[k].remove(responder)
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

    def add_object(self, object: GameObject):
        """Add a game object to this game."""
        if object is not None:
            if not (hasattr(object, 'update') and hasattr(object, 'draw')):
                raise ValueError("Game objects must have update() and draw().")
            self.__game_objects.append(object)
            self.__game_objects = sorted(self.__game_objects,
                                         key=lambda obj: obj.priority)
