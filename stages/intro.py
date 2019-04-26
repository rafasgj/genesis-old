"""Define the introduction screen."""

from engine import GameFont

import pygame


def create_scene(game_config):
    """Return the scene configuration."""
    width, height = canvas_size = game_config['canvas_size']
    initial_screen = {
        "name": "intro",
        "objects": {
            "background": {  # starfield
                "class": "objects.starfield.Starfield",
                "init": {"canvas_size": canvas_size}
            },
            "genesis": {
                "class": "engine.text.Label",
                "init": {
                    "font": GameFont("genesis.large"),
                    "text": "Genesis",
                    "position": (0, 0, width, height // 2),
                    "centered": True
                }
            },
            "press_space": {
                "class": "engine.text.Label",
                "init": {
                    "font": GameFont("genesis.normal"),
                    "text": "Press SPACE to Start",
                    "position": (0, height // 2, width, height),
                    "centered": True
                }
            },
            "score": {
                "class": "objects.score.Score",
                "init": {
                    "font": GameFont("genesis.normal"),
                    "position": (20, 5)
                }
            }
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
