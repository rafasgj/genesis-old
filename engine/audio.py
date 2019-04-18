"""Audio functions."""

import pygame


class Audio:
    """Provides several audio services."""

    @classmethod
    def init(self):
        """Initialize sound subsystem."""
        pygame.mixer.init()
        Audio.__loops = {}

    @classmethod
    def set_audio(self, name, filename):
        """Set an audio file."""
        Audio.__loops[name] = pygame.mixer.Sound(filename)

    @classmethod
    def play_audio(self, name, filename=None):
        """Play an audio file."""
        loop = Audio.__loops.get(name, None)
        if filename is not None:
            loop = Audio.__loops[name] = pygame.mixer.Sound(filename)
        if loop is not None:
            loop.play()

    @classmethod
    def play_audio_loop(cls, name, filename=None):
        """Play an audio file."""
        Audio.stop_audio_loop(name)
        loop = Audio.__loops.get(name, None)
        if filename is not None:
            loop = Audio.__loops[name] = pygame.mixer.Sound(filename)
        if loop is not None:
            loop.play(-1)

    @classmethod
    def stop_audio_loop(cls, name):
        """Play an audio file."""
        loop = Audio.__loops.get(name, None)
        if loop is not None:
            loop.stop()

    @classmethod
    def stop(cls):
        """Stop all sounds."""
        pygame.mixer.stop()
