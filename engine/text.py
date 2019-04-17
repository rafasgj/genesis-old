"""Draw text on screen."""

import pygame

from .gameobject import GameObject


class GameFont:
    """Models a Text Font to use on the game."""

    class GameText(GameObject):
        """Models an UI text object."""

        def __init__(self, surface, rect):
            """Initialize a text object."""
            GameObject.__init__(self, GameObject.Priority.UI)
            self.__surface = surface
            self.__rect = rect
            self.__blink_state = True
            self.visible = True

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

    REGULAR = (False, False)
    BOLD = (True, False)
    ITALIC = (False, True)
    BOLDITALIC = (True, True)

    def __init__(self, name, size, modifiers=REGULAR):
        """Initialize font object."""
        self.__font = pygame.font.Font(name, size)

    def __create_surface(self, text, **kwargs):
        color = kwargs.get('color', (255, 255, 255))
        surface = self.__font.render(text, True, color)
        return surface, surface.get_rect()

    def render_text(self, text, position, **kwargs):
        """Create a game text object."""
        surface, r = self.__create_surface(text, **kwargs)
        r.x, r.y = position
        return GameFont.GameText(surface, r)

    def render_text_centered(self, text, rect, **kwargs):
        """Create a game text object."""
        x, y, w, h = rect
        surface, r = self.__create_surface(text, **kwargs)
        r.centerx, r.centery = ((x + w) // 2, (y + h) // 2)
        return GameFont.GameText(surface, r)
