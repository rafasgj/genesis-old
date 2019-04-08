"""Genesis: The Game."""

from engine.game import Game
from engine.window import Window
from starfield import Starfield

import pygame
pygame.init()

window = Window()
game = Game(fps=60).set_window(window)
game.add_object(Starfield(window.size))
game.run()
