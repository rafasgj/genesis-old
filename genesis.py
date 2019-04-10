"""Genesis: The Game."""

from config import config

from engine.game import Game
from engine.window import Window
from engine.sprite import Sprite
from starfield import Starfield
from objects.enemy import Enemy, Wave
from random import randrange

import pygame
pygame.init()


def move(event):
    """Move player with directional keys."""
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    dy = -1 if keys[pygame.K_UP] else 0
    dy = dy + 1 if keys[pygame.K_DOWN] else dy
    dx = -1 if keys[pygame.K_LEFT] else 0
    dx = dx + 1 if keys[pygame.K_RIGHT] else dx
    player.move = (dx * config.player_speed, dy * config.player_speed)


if __name__ == "__main__":
    game = Game(fps=config.fps)
    game.window = Window()
    width, height = game.window.size

    game.on_key((pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT),
                move)

    game.add_object(Starfield(game.window.size))

    ufo = Enemy((width, height), 'media/images/ufo_spin.gif', randrange(5),
                animate=True)

    player = Sprite('media/images/f18.png', (200, 400))
    game.add_object(player)
    game.add_object(Sprite('media/images/ufo_big.gif', (600, 100), scale=0.8))
    # for e in range(10):
    #     ufo = Enemy((width, height), 'media/images/ufo_spin.gif', randrange(5),
    #                 animate=True)
    #     game.add_object(ufo)
    game.add_object(Wave(6, 5, (width, height)))

    game.run()
