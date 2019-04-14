"""Genesis: The Game."""

from config import config
from engine.game import Game
from engine.window import Window
from engine.sprite import Sprite
from engine.gameobject import GameObject
from engine.controllers import SinController
from objects.starfield import Starfield
from objects.enemy import Enemy, Wave
from objects.asteroid import Asteroid
from objects.player import Player

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

    controller = SinController(width, 5, 50, 5)
    # controller = InvertedSigmoidController(width, 100, speed=5)
    ufo = Enemy((width, height), 'media/images/ufo_spin.gif',
                controller=controller, animate=True)

    player = Player((200, 400))
    game.add_object(player)
    # game.add_object(Wave(6, lambda: SinController(width, 5, 50, 5), size))
    game.add_object(Asteroid((width, height // 2), 0.5))
    game.add_object(ufo)

    game.run()
