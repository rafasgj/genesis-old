"""Genesis Splash Screen Demo."""

from engine import Game, Window
import stages.intro

import pygame
pygame.init()


game = Game(fps=60)
game.window = Window(fullscren=True)

script = stages.intro.create_scene({"canvas_size": game.window.size})

game.run(script)

