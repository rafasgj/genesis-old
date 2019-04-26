"""Audio functions."""

import pygame
pygame.mixer.init()


class Mixer:
    """Provides several audio services."""

    def __init__(self, config={}):
        """Initialize mixer."""
        self.__loops = {}
        self.__mute = config.get('mute', False)

    def update_config(self, **kwargs):
        """Add audio configuration."""
        self.__mute = kwargs.get('mute', False)

    def add(self, name, filename):
        """Set an audio file."""
        self.__loops[name] = pygame.mixer.Sound(filename)

    def play_loop(self, name):
        """Play an audio file."""
        self.play(name, -1)

    def stop(self, name=None):
        """Play an audio file."""
        if name is None:
            pygame.mixer.stop()
        else:
            self.__get_loop(name).stop()

    def __get_loop(self, name):
        loop = self.__loops.get(name, None)
        if loop is None:
            raise Exception("{} audio is not set.".format(name))
        return loop

    def play(self, name, *args, **kwargs):
        """Play an audio loop."""
        if not self.__mute:
            self.__get_loop(name).play(*args, **kwargs)
