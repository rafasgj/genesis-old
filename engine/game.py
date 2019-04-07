"""The base game class."""

import pygame


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
        self.__keymap = {
            pygame.K_ESCAPE: lambda e: self.stop(),
        }

    def stop(self):
        """Stop running the game."""
        self.running = False

    def __keydown(self, event):
        """Handle keyboard press events."""
        if event.key != pygame.K_ESCAPE:
            self.__keymap.get(event.key, Game.__ignore_event)(Game.KEYDOWN)

    def __keyup(self, event):
        """Handle keyboard release events."""
        self.__keymap.get(event.key, Game.__ignore_event)(Game.KEYUP)

    def run(self):
        """Start the game loop."""
        self.running = True
        while self.running:
            # handle events
            for event in pygame.event.get():
                self.__events.get(event.type, Game.__ignore_event)(event)
            # update objects
            for object in self.__game_objects:
                object.update()
            # draw objects
            self.__window.clear()
            for object in self.__game_objects:
                self.__window.draw(object)
            # swap buffers
            pygame.display.update()
            # ensure loop do not run faster than FPS.
            self.__clock.tick(self.__fps)

    def on_key(self, key, responder):
        """Define a responder for a keyboard event."""
        # we'll save ESCAPE to always quit the game, useful on fullscreen...
        if key == pygame.K_ESCAPE:
            return
        self.__keymap[key] = responder
        return self

    def set_window(self, w):
        """Set the game window, if not set. It is a write-only property."""
        if not hasattr(self, "__window"):
            self.__window = w
        return self

    def add_object(self, object):
        """Add a game object to this game."""
        if object is not None:
            if not (hasattr(object, 'update') and hasattr(object, 'draw')):
                raise ValueError("Game objects must have update() and draw().")
            self.__game_objects.append(object)
