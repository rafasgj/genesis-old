"""Define a Stamp than can be used on the game multiple times."""

from engine import GameObject


class Stamp(GameObject):
    """Models a text stamp."""

    def __init__(self, font, text, **kwargs):
        """Initialize the game object."""
        GameObject.__init__(self, GameObject.Priority.BACKGROUND.value - 10)
        self.__blink_state = True
        self.visible = True
        self.__surface, self.__rect = font.render(font, text, **kwargs)
        self.__stamps = []

    def update(self, bounds):
        """No need to update."""
        pass

    def draw(self, screen):
        """Draw stamps."""
        for stamp in self.__stamps:
            screen.blit(self.__surface, stamp)

    def stamp(self, positions, **kwargs):
        """Move label to the given position."""
        if not isinstance(positions, list):
            positions = [positions]
        for position in positions:
            x, y, *dim = position
            r = self.__rect.copy()
            if kwargs.get('centered', False):
                w, h = dim
                r.centerx, r.centery = ((x + w) // 2, (y + h) // 2)
            else:
                r.x, r.y = x, y
            self.__stamps.append(r)

    def remove(self, index):
        """Remove a stamp."""
        del(self.__stamps[index])
