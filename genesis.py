"""Genesis: The Game."""

from config import config
from engine import Game, SinController, Window
from objects import Starfield, Enemy, Asteroid, Player, Shot

from random import randint

import pygame
pygame.init()


def KeyboardController(game, keys):
    """Define a Keyboard controller."""
    def player_move(event):
        """Move player with directional keys."""
        nonlocal move, space_not_pressed
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        dy = -1 if keys[pygame.K_UP] else 0
        dy = dy + 1 if keys[pygame.K_DOWN] else dy
        dx = -1 if keys[pygame.K_LEFT] else 0
        dx = dx + 1 if keys[pygame.K_RIGHT] else dx
        move = (dx * config.player_speed, dy * config.player_speed)

        if keys[pygame.K_SPACE]:
            x, y, w, _ = player.bounds
            cx, cy, *_ = asteroid.bounds
            game.add_object(Shot((x + w, y), (cx, cy)))
            space_not_pressed = False
        else:
            space_not_pressed = True

    space_not_pressed = True
    move = (0, 0)
    game.on_key(keys, player_move)
    while True:
        yield move


if __name__ == "__main__":
    game = Game(fps=config.fps)
    game.window = Window(size=(800, 600))
    width, height = size = game.window.size

    game.add_object(Starfield(game.window.size))

    controller = SinController(width, 1, 4, 3)
    # controller = InvertedSigmoidController(width, 100, speed=5)

    keys = (pygame.K_UP, pygame.K_DOWN,
            pygame.K_LEFT, pygame.K_RIGHT,
            pygame.K_SPACE)
    player = Player((200, 400), controller=KeyboardController(game, keys))
    game.add_object(player)

    asteroid = Asteroid((width, height // 2), 0.5)
    game.add_object(asteroid)

    ufo = Enemy(size, 'media/images/ufo_spin.gif',
                controller=controller, animate=True)
    game.add_object(ufo)

    wy = randint(0, height)
    wave = [Enemy(size, 'media/images/ufo_spin.gif',
                  controller=controller, animate=True,
                  position=(width + (i + 1) * 70, wy))
            for i in range(6)]
    for e in wave:
        game.add_object(e)

    game.run()
