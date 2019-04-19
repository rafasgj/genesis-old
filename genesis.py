"""Genesis: The Game."""

from config import config
from objects import Player
from engine import Game, Window, KeyboardController, Font
from objects.score import Score

import stages.intro, stages.stage1

import pygame
pygame.init()


if __name__ == "__main__":
    import sys

    game = Game(fps=config.fps)

    mixer_config = {"mute": "-m" in sys.argv}

    if "-w" in sys.argv:
        game.window = Window(size=(800, 600))
    else:
        game.window = Window(fullscreen=True)

    def _player_shoot(event, scene):
        if event.key == pygame.K_SPACE and event.type == pygame.KEYDOWN:
            player = scene.get_object("player")
            if player.visible:
                x, y, w, _ = player.bounds
                origin = (x + w - 15, y + 10)
                target = (x + 2 * w, y + 10)
                color = (230, 0, 230)
                scene.event("spawn", "projectile",
                            init={
                                "creator": player,
                                "origin": origin,
                                "target": target,
                                "color": color
                            })
                scene.event("play", "player_shoot")

    directional = (pygame.K_UP, pygame.K_DOWN,
                   pygame.K_LEFT, pygame.K_RIGHT)
    kbd = KeyboardController(game, directional,
                             {pygame.K_SPACE: _player_shoot})
    player = Player((200, 400), controller=kbd, speed=config.player_speed)
    font = Font('media/fonts/open-24-display-st.ttf', 64)

    globals = {
        "canvas_size": game.window.size,
        "mixer_config": mixer_config,
        "player": player,
        "score": Score(font, (20, 5)),
        "text_font": font,
    }

    script = stages.intro.create_scene(globals)
    stage_1 = stages.stage1.create_scene(globals)
    script['next_scene'] = stage_1

    game.run(script)
