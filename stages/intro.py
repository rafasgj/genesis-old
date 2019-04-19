"""Define the introduction screen."""

from engine import Font, Label

import pygame


def create_scene(globals):
    """Return the scene configuration."""
    width, height = canvas_size = globals['canvas_size']
    bottom_half = (0, height // 2, width, height)
    msg = "Press SPACE to start"
    press_space = Label(globals['text_font'], msg, bottom_half, centered=True)
    initial_screen = {
        "mixer": {
            "config": globals['mixer_config'],
            "loops": {
                "background_music": 'media/sound/Androids.ogg',
            }
        },
        "objects": {
            "background": {  # starfield
                "class": "objects.starfield.Starfield",
                "init": {"size": canvas_size}
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
            "score": globals['score']
        },
        "events": [(350, 350, "object", "press_space", "blink")],
        "before": [
            ("spawn", "background"),
            ("spawn", "genesis"),
            ("spawn", "press_space"),
            ("spawn", "score"),
            ("object", "score", "toggle_score")
        ],
        "on_key": [(pygame.K_SPACE, "end_scene")]
    }
    return initial_screen
