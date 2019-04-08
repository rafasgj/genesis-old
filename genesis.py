"""Genesis: The Game."""

from config import config

from engine.game import Game
from engine.window import Window
from engine.sprite import Sprite
from starfield import Starfield

import pygame
pygame.init()


def move(event):
    """Move player with directional keys."""
    print(event.key)
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    dy = -1 if keys[pygame.K_UP] else 0
    dy = dy + 1 if keys[pygame.K_DOWN] else dy
    dx = -1 if keys[pygame.K_LEFT] else 0
    dx = dx + 1 if keys[pygame.K_RIGHT] else dx
    player.move = (dx * config.player_speed, dy * config.player_speed)


if __name__ == "__main__":
    window = Window()
    game = Game(fps=config.fps).set_window(window)

    game.on_key((pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT),
                move)

    game.add_object(Starfield(window.size))

    player = Sprite('media/images/f18.png', (200, 400))
    game.add_object(player)
    game.add_object(Sprite('media/images/ufo_big.gif', (600, 100), scale=0.8))
    game.add_object(Sprite('media/images/ufo_spin.gif', (400, 500),
                    animated=True))

    game.run()
