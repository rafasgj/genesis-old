"""Implement object controllers."""

from math import pi, sin, exp
import pygame


def KeyboardController(game, directional, special: dict):
    """Define a Keyboard controller."""
    move = (0, 0)
    up, down, left, right = directional

    def player_move(event, scene):
        """Move player with directional keys."""
        nonlocal move  # , up, down, left, right

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        dy = -1 if keys[up] else 0
        dy = dy + 1 if keys[down] else dy
        dx = -1 if keys[left] else 0
        dx = dx + 1 if keys[right] else dx
        move = (dx, dy)

    game.on_key(directional, player_move)
    for key, handler in special.items():
        game.on_key(key, handler)
    while True:
        yield move


def ConstantController(dx, dy, speed=1):
    """Define a controller that moves the object in a straight line."""
    while True:
        yield (dx * speed, dy * speed)


def SinController(length, freq, amp, speed=1, vertical=False):
    """Define a controller that moves the object in a straight line."""
    i = 0
    rad = pi
    factor = freq * 2 / length * rad
    while True:
        next = amp * sin(factor * i)
        value = next
        yield (speed, value) if not vertical else (value, speed)
        i += speed


def __sigmoid(x, temperature, length):
    factor = 20 / length
    expoent = -(x * factor - 10)
    return (1 / (exp(expoent / temperature) + 1))


def SigmoidController(length, amp, temperature=1, speed=1, vertical=False):
    """Define a controller that moves the object in a straight line."""
    x = 0
    last = 0
    while True:
        next = amp * (2 * __sigmoid(x, temperature, length) - 1)
        value = (next - last)
        yield (speed, value) if not vertical else (value, speed)
        last = next
        x += speed


def SigmoidPrimeController(length, amp, temp=1, speed=1, vertical=False):
    """Define a controller that moves the object in a straight line."""
    x = 0
    last = 0
    while True:
        sigp = __sigmoid(x, temp, length)
        next = amp * 4 * (sigp * (1 - sigp))
        value = (next - last)
        yield (speed, value) if not vertical else (value, speed)
        last = next
        x += speed


def InvertedSigmoidController(length, amp, temp=1, speed=1, vertical=False):
    """Define a controller that moves the object in a straight line."""
    x = 0
    last = 0
    while True:
        next = amp * (1 - (2 * __sigmoid(x, temp, length) - 1))
        value = (next - last)
        yield (speed, value) if not vertical else (value, speed)
        last = next
        x += speed
