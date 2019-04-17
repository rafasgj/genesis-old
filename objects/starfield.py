"""Creates a 2D starfield, with parallax effect."""

from engine import GameObject

from random import randrange, choice
import pygame


class Starfield(GameObject):
    """Define a starfield background, with parallax."""

    def __create_star(self, x):
        """Create a star for the background parallax."""
        # a star is (x, y, speed, magnitude, color)
        return [x, randrange(0, self.__height - 1), choice([2, 4, 6]),
                choice([1, 2, 3]), (choice([100, 200, 250]),) * 3]

    def __init__(self, size, count=300):
        """Create the starfield stars."""
        GameObject.__init__(self, GameObject.Priority.BACKGROUND)
        self.__width, self.__height = size
        self.__stars = [self.__create_star(randrange(0, self.__width - 1))
                        for star in range(count)]

    def update(self, canvas_size):
        """Move the stars in the starfield."""
        self.__stars = [[x - speed, y, speed, mag, color]
                        if x - speed > 0
                        else self.__create_star(self.__width)
                        for x, y, speed, mag, color in self.__stars]

    def draw(self, surface):
        """Draw the starfield in a screen."""
        for x, y, _, magnitude, color in self.__stars:
            # rect = (x, y, magnitude, magnitude)
            pygame.draw.circle(surface, color, (x, y), magnitude)
