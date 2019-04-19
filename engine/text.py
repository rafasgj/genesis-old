"""Draw text on screen."""

import pygame

from .gameobject import GameObject


class Label(GameObject):
    """Models an UI text object."""

    def __init__(self, font, text, position, **kwargs):
        """Initialize a text object."""
        GameObject.__init__(self, GameObject.Priority.UI)
        self.__blink_state = True
        self.visible = True
        self.__surface, r = font.render(font, text, **kwargs)
        x, y, *dim = position
        if kwargs.get('centered', False):
            w, h = dim
            r.centerx, r.centery = ((x + w) // 2, (y + h) // 2)
        else:
            r.x, r.y = x, y
        self.__rect = r

    def hide(self):
        """Hide the object."""
        self.visible = False

    def update(self, bounds):
        """Update object."""
        pass

    def draw(self, screen):
        """Draw on the screen."""
        if self.visible and self.__blink_state:
            screen.blit(self.__surface, self.__rect)

    def blink(self, *args, **kwargs):
        """Toggle blink state."""
        self.__blink_state = not self.__blink_state


class Font:
    """Models a Text Font to use on the game."""

    REGULAR = (False, False)
    BOLD = (True, False)
    ITALIC = (False, True)
    BOLDITALIC = (True, True)

    def __init__(self, name, size, modifiers=REGULAR):
        """Initialize font object."""
        self.__font = pygame.font.Font(name, size)

    def __create_surface(self, font, text, **kwargs):
        color = kwargs.get('color', (255, 255, 255))
        surface = self.__font.render(text, True, color)
        return surface, surface.get_rect()

    def render(self, text, color, **kwargs):
        """Render a text with the given color."""
        return self.__create_surface(text, color, **kwargs)
