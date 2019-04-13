"""Models a simple NPC."""

from engine.sprite import Sprite
from random import randint
from engine.behaviors import Controllable
from engine.gameobject import GameObject


class Enemy(Controllable, GameObject):
    """Models a simple NPC."""

    def __init__(self, canvas_size, image, controller=None, animate=False):
        """Initialize Enemy object."""
        x, y = canvas_size
        sy = randint(50, y - 50)
        self.sprite = Sprite(image, (x, sy), animate=animate, cast_shadow=True)
        self.behavior = controller

    def update(self):
        """Update enemy position."""
        try:
            dx, dy = next(self.behavior)
            dx *= -1
            self.sprite.move = (dx, dy)
        except Exception as e:
            print(e)
            self.sprite.move = (0, 0)
        self.sprite.update()

    def draw(self, screen):
        """Draw enemy on the screen."""
        self.sprite.draw(screen)

    @property
    def position(self):
        """Return the enemy position."""
        return self.sprite.position


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
