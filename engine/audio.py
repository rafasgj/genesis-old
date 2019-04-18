"""Audio functions."""

import pygame


class Audio:
    """Provides several audio services."""

    @classmethod
    def init(cls):
        """Initialize sound subsystem."""
        pygame.mixer.init()
        Audio.__loops = {}
        Audio.__config = {}

    @classmethod
    def config(cls, **kwargs):
        """Add audio configuration."""
        Audio.__config.uupdate(kwargs)

    @classmethod
    def set_audio(cls, name, filename):
        """Set an audio file."""
        Audio.__loops[name] = pygame.mixer.Sound(filename)

    @classmethod
    def play_audio(cls, name, filename=None):
        """Play an audio file."""
        loop = Audio.__loops.get(name, None)
        if filename is not None:
            loop = Audio.__loops[name] = pygame.mixer.Sound(filename)
        if loop is not None:
            Audio.__play(loop)

    @classmethod
    def play_audio_loop(cls, name, filename=None):
        """Play an audio file."""
        Audio.stop_audio_loop(name)
        loop = Audio.__loops.get(name, None)
        if filename is not None:
            loop = Audio.__loops[name] = pygame.mixer.Sound(filename)
        if loop is not None:
            Audio.__play(loop, -1)

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

    @classmethod
    def __play(cls, audio, *args):
        if not Audio.__config.get('mute', False):
            audio.play(*args)
