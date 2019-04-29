"""Draw text on screen."""

import pygame

from .gameobject import GameObject


class Label(GameObject):
    """Models an UI text object."""

    def __init__(self, font, text, position, **kwargs):
        """Initialize a text object."""
        GameObject.__init__(self, GameObject.Priority.UI)
        kwargs.update({} if 'color' in kwargs else {'color': (255, 255, 255)})
        self.__blink_state = True
        self.visible = True
        self.__surface, self.__rect = font.render(text, **kwargs)
        self.move_to(position, **kwargs)

    def hide(self):
        """Hide the object."""
        self.visible = False

    def update(self, bounds):
        """Update object."""
        pass

    def move_to(self, position, **kwargs):
        """Move label to the given position."""
        x, y, *dim = position
        r = self.__rect
        if kwargs.get('centered', False):
            w, h = dim
            r.centerx, r.centery = ((x + w) // 2, (y + h) // 2)
        else:
            r.x, r.y = x, y
        self.__rect = r

    def draw(self, screen):
        """Draw on the screen."""
        if self.visible and self.__blink_state:
            screen.blit(self.__surface, self.__rect)

    def blink(self, *args, **kwargs):
        """Toggle blink state."""
        self.__blink_state = not self.__blink_state

    @property
    def bounds(self):
        """Retrieve lable surface boundaries."""
        return self.__rect

    @bounds.setter
    def bounds(self, rect):
        """Set label boundaries."""
        self.__rect = rect


class Font:
    """Models a Text Font to use on the game."""

    REGULAR = (False, False)
    BOLD = (True, False)
    ITALIC = (False, True)
    BOLDITALIC = (True, True)

    def __init__(self, filename, size, modifiers=REGULAR):
        """Initialize font object."""
        self.__font = pygame.font.Font(filename, size)

    def __create_surface(self, text, **kwargs):
        color = kwargs.get('color', (255, 255, 255))
        surface = self.__font.render(text, True, color)
        return surface, surface.get_rect()

    def render(self, text, **kwargs):
        """Render a text with the given color."""
        return self.__create_surface(text, **kwargs)
