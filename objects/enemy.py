"""Models a simple NPC."""

from random import randint
from engine import (Sprite, Controllable, Movable, GameObject,
                    ConstantController, Collider)
from .player import Player
from .projectile import Projectile
from .explosion import Explosion
from .killable import Killable


class Enemy(Controllable, Collider, Movable, GameObject):
    """Models a simple NPC."""

    def __init__(self, canvas, image, **kw):
        """Initialize Enemy object."""
        Controllable.__init__(self,
                              kw.get('controller',
                                     ConstantController(-1, 0)))
        Collider.__init__(self, kw.get('bounding_shape', Collider.RECT))
        Movable.__init__(self, kw.get('position', (canvas[0] + 10,
                                      randint(50, canvas[1] - 50))))
        GameObject.__init__(self, kw.get('priority', GameObject.Priority.NPC))
        self.__sprite = Sprite(image, **kw)
        x, y, *_ = self.__sprite.bounds
        self.move(x, y)

    def update(self, bounds):
        """Update enemy position."""
        try:
            dx, dy = next(self.controller)
            dx *= -1
            self.move(dx, dy)
            self.offlimits(bounds)
        except Exception as e:
            pass
        x, _, w, *_ = self.bounds
        if x + 2 * w < 0:
            self.destroy()

    def draw(self, screen):
        """Draw enemy on the screen."""
        self.__sprite.draw(screen, self.position)

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
        """Indestructible enemy."""
        pass

    @property
    def center(self):
        """Query object bounds."""
        return tuple(map(lambda e: sum(e),
                         zip(self.position, self.__sprite.center)))

    @property
    def rotation(self):
        """Return the sprite rotation."""
        return self.__sprite.rotation

    @property
    def dimension(self):
        """Return the object dimension."""
        _, _, w, h, *_ = self.__sprite.bounds
        return (w, h)


class KillableEnemy(Enemy, Killable):
    """Models an enemy that can be killed."""

    def __init__(self, canvas, image, **kw):
        """Initialize Killable Enemy object."""
        Enemy.__init__(self, canvas, image, **kw)
        Killable.__init__(self, Explosion.SMALL, time_scale=0.5)

    def draw(self, screen):
        """Draw enemy on the screen."""
        if self.should_update:
            Enemy.draw(self, screen)
        else:
            Killable.draw(self, screen)

    def update(self, bounds):
        """Update enemy position."""
        if self.should_update:
            Enemy.update(self, bounds)
        else:
            Killable.update(self, bounds)

    def collide_with(self, object):
        """Enemy wal killed."""
        if self.should_update:
            will_die = isinstance(object, Projectile) and \
                not isinstance(self, object.creator)
            if will_die or isinstance(object, Player):
                self.die()
                self.should_collide = False
