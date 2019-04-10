"""Models a simple NPC."""

from math import exp
from engine.sprite import Sprite
from random import random, randint


def __get_sigmoid_derivative(self, size, amplitude, **kwargs):
    temperature = kwargs.get('temperature', 1)
    width = size[0]
    factor = 20 / width
    x, _ = self.position
    x = (x * factor) - 10
    ex = 1 / (exp(-x / temperature) + 1)
    return 4 * (ex * (1 - ex))


def sigmoid(self, size, amplitude, **kwargs):
    """Return a sigmoid behavior."""
    dx = -self.sprite.speed
    dy = amplitude * __get_sigmoid_derivative(self, size, amplitude, **kwargs)
    return (dx, dy)


def inv_sigmoid(self, size, amplitude, **kwargs):
    """Return an inverted sigmoid behavior."""
    dx = -self.sprite.speed
    sd = __get_sigmoid_derivative(self, size, amplitude, **kwargs)
    dy = amplitude * (1 - sd)
    return (dx, dy - amplitude)


class Enemy:
    """Models a simple NPC."""

    def __init__(self, canvas_size, image, speed=1, amp=1, animate=False):
        """Initialize Enemy object."""
        x, y = canvas_size
        sy = randint(50, y - 50)
        self.sprite = Sprite(image, (x, sy), speed=speed,
                             animate=animate, cast_shadow=True)
        fn = sigmoid if sy > y // 2 else inv_sigmoid
        self.behavior = lambda: fn(self, canvas_size, amp)

    def update(self):
        """Update enemy position."""
        self.sprite.move = self.behavior()
        self.sprite.update()

    def draw(self, screen):
        """Draw enemy on the screen."""
        self.sprite.draw(screen)

    @property
    def position(self):
        """Return the enemy position."""
        return self.sprite.position


class Wave:
    """Define a wave of enemies."""

    def __init__(self, count, speed_factor, canvas_size):
        """Initialize an enemy wave."""
        spd = 1 + random() * speed_factor
        self.enemies = [Enemy(canvas_size, 'media/images/ufo_spin.gif',
                              spd, 1 + random(), True)
                        for _ in range(count)]
        y = self.enemies[0].sprite.position[1]
        for i, e in enumerate(self.enemies):
            x, _ = e.position
            e.sprite.position = (x + 100 * i, y)

    def update(self):
        """Update all the enemies in the wave, if they are visible."""
        [e.update() for e in self.enemies]

    def draw(self, screen):
        """Draw all the enemies if they are visible."""
        [e.draw(screen) for e in self.enemies]

    def limits(self, canvas_size):
        """Verify limit for all enemies."""
        [e.limits(canvas_size) for e in self.enemies]
