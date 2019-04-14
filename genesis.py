"""Genesis: The Game."""

from config import config
from engine.game import Game
from engine.window import Window
from engine.controllers import SinController
from objects.starfield import Starfield
from objects.enemy import Enemy
from objects.asteroid import Asteroid
from objects.player import Player

from random import randint

import pygame
pygame.init()


def player_move(event):
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
    game.window = Window(size=(800, 600))
    width, height = size = game.window.size

    game.on_key((pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT),
                player_move)

    game.add_object(Starfield(game.window.size))

    controller = SinController(width, 1, 1, 1)
    # controller = InvertedSigmoidController(width, 100, speed=5)
    ufo = Enemy(size, 'media/images/ufo_spin.gif',
                controller=controller, animate=True)

    player = Player((200, 400))
    game.add_object(player)

    wy = randint(0, height)
    wave = [Enemy(size, 'media/images/ufo_spin.gif',
                  controller=controller, animate=True,
                  position=(width + (i + 1) * 70, wy))
            for i in range(6)]
    for e in wave:
        game.add_object(e)
    game.add_object(Asteroid((width, height // 2), 0.5))
    game.add_object(ufo)

    game.run()
