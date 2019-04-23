"""Define the introduction screen."""

from engine import Font, Label

from objects.score import Score

import pygame


def create_scene(game_config):
    """Return the scene configuration."""
    width, height = canvas_size = game_config['canvas_size']
    bottom_half = (0, height // 2, width, height)
    font_file = 'media/fonts/open-24-display-st.ttf'
    font = game_config.get('text_font', Font(font_file, 64))
    msg = "Press SPACE to start"
    press_space = Label(font, msg, bottom_half, centered=True)
    initial_screen = {
        "name": "intro",
        "mixer": {
            "config": game_config.get('mixer_config', {}),
            "loops": {
                "background_music": 'media/sound/Androids.ogg',
            }
        },
        "objects": {
            "background": {  # starfield
                "class": "objects.starfield.Starfield",
                "init": {"canvas_size": canvas_size}
            },
            "genesis": {
                "class": "engine.text.Label",
                "init": {
                    "font": Font('media/fonts/open-24-display-st.ttf', 256),
                    "text": "Genesis",
                    "position": (0, 0, width, height // 2),
                    "centered": True
                }
            },
            "press_space": press_space,
            "score": game_config.get('score', Score(font, (20, 5)))
        },
        "events": [(350, 350, "object", "press_space", "blink")],
        "before": [
            ("spawn", ["background", "genesis", "press_space", "score"]),
            ("object", "score", "toggle_score")
        ],
        "on_key": {
            (pygame.K_SPACE, "end_scene"),
        },
        "next_scene": {
            "end_scene": "stage1",
            "game_over": "game_over"
        }
    }
    return initial_screen
