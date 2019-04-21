"""Genesis Splash Screen Demo."""

from engine import Game, Window
import stages.intro

import pygame
pygame.init()


options = cli_parser.proccess_CLI()

mx = sorted(pygame.display.list_modes())[-1]
size = options.dimension if options.dimension else mx
game = Game(fps=60)
game.window = Window(size=size,
                     fullscreen=not options.windowed)
config = {
    "canvas_size": game.window.size,
    "mixer": {"mute": options.mute}
}
game.add_scene(stages.intro.create_scene(config))
game.run("intro")
