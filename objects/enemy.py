"""Models a simple NPC."""

from engine.sprite import Sprite
from random import randint
from engine.behaviors import Controllable
from engine.gameobject import GameObject
from engine.controllers import ConstantController
from engine.collider import Collider
from .player import Player


class Enemy(Controllable, Collider, GameObject):
    """Models a simple NPC."""

    def __init__(self, canvas, image, **kw):
        """Initialize Enemy object."""
        Controllable.__init__(self,
                              kw.get('controller',
                                     ConstantController(-1, 0)))
        Collider.__init__(self, kw.get('shape', Collider.RECT))
        GameObject.__init__(self, GameObject.Priority.NPC)
        x, y = canvas
        sy = randint(50, y - 50)
        self.__sprite = Sprite(image, (x, sy),
                               animate=kw.get('animate', False),
                               cast_shadow=kw.get('cast_shadow', True))
        self.__visible = True

    def update(self):
        """Update enemy position."""
        if self.visible:
            try:
                dx, dy = next(self.controller)
                dx *= -1
                self.__sprite.move = (dx, dy)
            except Exception as e:
                self.__sprite.move = (0, 0)
            self.__sprite.update()

    def draw(self, screen):
        """Draw enemy on the screen."""
        if self.visible:
            self.__sprite.draw(screen)

    def collide_with(self, object):
        """Enemy wal killed."""
        if isinstance(object, Player):
            self.__visible = False

    @property
    def visible(self):
        """Retrieve if object is visible or not."""
        return self.__visible

    @property
    def position(self):
        """Return the enemy position."""
        return self.sprite.position

    @property
    def bounds(self):
        """Query object bounds."""
        return self.__sprite.bounds


class Wave:
    """Define a wave of enemies."""

    def __init__(self, count, controller_factory, canvas_size):
        """Initialize an enemy wave."""
        self.enemies = [Enemy(canvas_size, 'media/images/ufo_spin.gif',
                              controller_factory(), True)
                        for _ in range(count)]
        y = self.enemies[0].sprite.position[1]
        for i, e in enumerate(self.enemies):
            x, _ = e.position
            e.sprite.position = (x + 100 * i, y)

    def update(self):
        """Update all the enemies in the wave, if they are visible."""
        for e in self.enemies:
            e.update()

    def draw(self, screen):
        """Draw all the enemies if they are visible."""
        for e in self.enemies:
            e.draw(screen)
