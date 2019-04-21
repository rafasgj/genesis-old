"""Genesis Splash Screen Demo."""

from engine import Game, Window
import stages.intro

import pygame
pygame.init()


game = Game(fps=60)
game.window = Window(size=(800, 600))
config = {
    "canvas_size": game.window.size
}
game.add_scene(stages.intro.create_scene(config))
game.run("intro")
