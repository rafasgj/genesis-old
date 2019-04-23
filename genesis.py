"""Genesis: The Game."""

from config import config
from engine import Game, Window, Font
from objects.score import Score

import stages.gameover, stages.intro, stages.stage1
import cli_parser

from random import randint

import pygame
pygame.init()

if __name__ == "__main__":
    game = Game(fps=config.fps)

    options = cli_parser.proccess_CLI()

    mx = sorted(pygame.display.list_modes())[-1]
    size = options.dimension if options.dimension else mx
    game.window = Window(size=size,
                         fullscreen=not options.windowed)
    config.canvas_size = game.window.size

    font = Font('media/fonts/open-24-display-st.ttf', 64)

    game_config = {
        "canvas_size": game.window.size,
        "mixer_config": {"mute": options.mute},
        "score": Score(font, (20, 5)),
        "text_font": font,
        'lives_left': config.number_of_lives
    }

    game.add_scene(stages.intro.create_scene(game_config))
    game.add_scene(stages.gameover.create_scene(game_config))
    game.add_scene(stages.stage1.create_scene(game_config))
    game.run("intro")


def update_score_enemy(sender, scene):
    """Update player score."""
    scene.get_object('score').add(50)
    scene.event("play", "enemy_kill")


def player_shoot(event, scene):
    """Create a projectile, where the player object is."""
    if event.key == pygame.K_SPACE and event.type == pygame.KEYDOWN:
        player = scene.get_object("player")
        if player.should_update:
            x, y, w, _ = player.bounds
            origin = (x + w - 15, y + 10)
            target = (x + 2 * w, y + 10)
            color = (230, 0, 230)
            scene.event("spawn", "projectile",
                        init={
                            "creator": player,
                            "origin": origin,
                            "target": target,
                            "color": color,
                            "size": 12
                        })
            scene.event("play", "player_shoot")


def enemy_shoot(scene):
    """Make an enemy shot the player."""
    tx, ty, *_ = scene.get_object('player').bounds
    lst = [u for u in scene.get_object_list("ufo") if u.is_alive]
    for ufo in lst:
        if randint(0, 100) < 5:
            color = (230, 0, 230)
            x, y, w, h = ufo.bounds
            origin = (x + w // 2, y + h // 2)
            target = (tx, ty)
            color = (0, 230, 230)
            scene.event("spawn", "projectile",
                        init={
                            "creator": ufo,
                            "origin": origin,
                            "target": target,
                            "color": color,
                            "size": 12
                        })
            scene.event("play", "player_shoot")


def player_dead(player, scene):
    """Player is dead."""
    scene.event("play", "player_kill")
    if player.lives == 0:
        scene.queue_event(6000, 0, "game_over")
    else:
        scene.queue_event(1500, 0, "object", "life_stamp", "remove", -1)
        scene.queue_event(4000, 0, "object", "player", "respawn")
