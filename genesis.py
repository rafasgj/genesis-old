"""Genesis: The Game."""

from config import config
from engine import Game, SinController, Window, GameFont, Audio
from objects import Starfield, Enemy, Asteroid, Player, Shot

from random import randint

import pygame
pygame.init()


def KeyboardController(game, keys):
    """Define a Keyboard controller."""
    def player_move(event):
        """Move player with directional keys."""
        nonlocal move
        global game, player

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            x, y, w, _ = player.bounds
            # cx, cy, *_ = asteroid.bounds
            game.add_object(Shot(player, (220, 0, 220),
                                 (x + w - 15, y + 10), (x + 2 * w, y + 10)))
            Audio.play_audio('player_shoot', 'media/sound/laser.ogg')

        dx, dy = 0, 0
        dy = -1 if keys[pygame.K_UP] else 0
        dy = dy + 1 if keys[pygame.K_DOWN] else dy
        dx = -1 if keys[pygame.K_LEFT] else 0
        dx = dx + 1 if keys[pygame.K_RIGHT] else dx
        move = (dx * config.player_speed, dy * config.player_speed)

    move = (0, 0)
    game.on_key(keys, player_move)
    while True:
        yield move


if __name__ == "__main__":
    import sys

    def _init_screen(*args):
        width, height = game.window.size
        game.start_scene()
        game.add_object(Starfield(game.window.size))

        title_font = GameFont('media/fonts/open-24-display-st.ttf', 256)
        text_font = GameFont('media/fonts/open-24-display-st.ttf', 64)
        top_half = (0, 0, width, height // 2)
        bottom_half = (0, height // 2, width, height)
        game_title = title_font.render_text_centered("Genesis", top_half)
        press_space = text_font.render_text_centered("Press SPACE to start",
                                                     bottom_half)
        game.add_timer(press_space.blink, 350)
        game.add_object(game_title)
        game.add_object(press_space)

        game.on_key([pygame.K_SPACE], _start_game)
        game.run()

    def _start_game(*args):
        game.remove_key([pygame.K_SPACE], _start_game)

        game.start_scene()

        width, height = size = game.window.size

        game.add_object(Starfield(game.window.size))

        controller = SinController(width, 1, 4, 3)
        # controller = InvertedSigmoidController(width, 100, speed=5)

        game.add_object(player)

        asteroid = Asteroid((width, height // 2), 0.5)
        game.add_object(asteroid)

        ufo = Enemy(size, 'media/images/ufo_spin.gif',
                    controller=controller, animate=True)
        game.add_object(ufo)

        wy = randint(0, height)
        wave = [Enemy(size, 'media/images/ufo_spin.gif',
                      controller=controller, animate=True,
                      position=(width + (i + 1) * 70, wy))
                for i in range(6)]
        for e in wave:
            game.add_object(e)

        Audio.play_audio_loop('background_music', 'media/sound/Androids.ogg')
        game.run()

    game = Game(fps=config.fps)
    if "-w" in sys.argv:
        game.window = Window(size=(800, 600))
    else:
        game.window = Window(fullscreen=True)
    keys = (pygame.K_UP, pygame.K_DOWN,
            pygame.K_LEFT, pygame.K_RIGHT,
            pygame.K_SPACE)
    kbd = KeyboardController(game, keys)
    player = Player((200, 400), controller=kbd)

    _init_screen(game)
