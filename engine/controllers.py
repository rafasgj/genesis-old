"""Implement object controllers."""

from math import pi, sin, exp


def ConstantController(dx, dy, speed=1):
    """Define a controller that moves the object in a straight line."""
    while True:
        yield (dx * speed, dy * speed)


def SinController(length, freq, amp, speed=1, vertical=False):
    """Define a controller that moves the object in a straight line."""
    last = 0
    i = 0
    rad = pi
    factor = freq * 2 / length * rad
    while True:
        next = amp * sin(factor * i)
        # value = (next - last)
        value = next
        yield (speed, value) if not vertical else (value, speed)
        last = next
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
