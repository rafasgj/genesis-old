"""Models a simple NPC."""

from random import randint
from engine import (Sprite, Controllable, Hideable, Movable,
                    GameObject, ConstantController, Collider)
from .player import Player
from .explosion import Explosion
from .killable import Killable


class Enemy(Controllable, Collider, Movable, Killable, GameObject):
    """Models a simple NPC."""

    def __init__(self, canvas, image, **kw):
        """Initialize Enemy object."""
        Controllable.__init__(self,
                              kw.get('controller',
                                     ConstantController(-1, 0)))
        Collider.__init__(self, kw.get('shape', Collider.RECT))
        Movable.__init__(self, kw.get('position', (canvas[0] + 10,
                                      randint(50, canvas[1] - 50))))
        Killable.__init__(self, Explosion.SMALL)
        GameObject.__init__(self, GameObject.Priority.NPC)
        self. __sprite = Sprite(image,
                                animate=kw.get('animate', False),
                                cast_shadow=kw.get('cast_shadow', True))

    def update(self, bounds):
        """Update enemy position."""
        if self.should_update:
            try:
                dx, dy = next(self.controller)
                dx *= -1
                self.move(dx, dy)
                self.offlimits(bounds)
            except Exception as e:
                pass
        else:
            Killable.update(self, bounds)

    def draw(self, screen):
        """Draw enemy on the screen."""
        if self.should_update:
            self.__sprite.draw(screen, self.position)
        else:
            Killable.draw(self, screen)

    def offlimits(self, limits):
        """Take action when object is off-limits, return if needs update."""
        wx, wy, ww, wh = limits
        x, y, w, h = self.bounds
        if x + w < wx:
            self.hide()
        dy = wy if y < wy else y
        dy = (wy + wh) - h if (y + h) > (wy + wh) else dy
        dy -= y
        self.move(0, dy)

    def collide_with(self, object):
        """Enemy wal killed."""
        if self.should_update:
            if isinstance(object, Player):
                self.die()

    @property
    def bounds(self):
        """Query object bounds."""
        x, y = self.position
        _, _, w, h = self.__sprite.bounds
        return (x, y, w, h)
