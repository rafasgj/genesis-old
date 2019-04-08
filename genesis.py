"""Genesis: The Game."""

from engine.game import Game
from engine.window import Window
from engine.sprite import Sprite
from starfield import Starfield

import pygame
pygame.init()


window = Window()
game = Game(fps=60).set_window(window)

game.add_object(Starfield(window.size))

game.add_object(Sprite('media/images/f18.png', (200, 400)))
game.add_object(Sprite('media/images/ufo_big.gif', (600, 100), scale=0.8))
game.add_object(Sprite('media/images/ufo_spin.gif', (400, 500), animated=True))

game.run()
