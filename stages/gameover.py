"""Define the end screen."""

from engine import GameFont


def create_scene(game_config):
    """Return the scene configuration."""
    width, height = canvas_size = game_config['canvas_size']
    scene = {
        "name": "game_over",
        "audio": {
            "background_music": {
                "filename": 'media/sound/Androids.ogg',
                "loop": True,
                "autostart": True
            }
        },
        "objects": {
            "background": {  # starfield
                "class": "objects.starfield.Starfield",
                "init": {"canvas_size": canvas_size}
            },
            "GAME": {
                "class": "engine.text.Label",
                "init": {
                    "font": GameFont('genesis.huge'),
                    "text": "GAME",
                    "position": (0, 0, width, height // 2),
                    "centered": True
                }
            },
            "OVER": {
                "class": "engine.text.Label",
                "init": {
                    "font": GameFont('genesis.huge'),
                    "text": "OVER",
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
        "events": [
            (2000, 2000, "object", "score", "toggle_score"),
            (8000, 0, "end_scene")
        ],
        "before": [
            ("spawn", "background"),
            ("spawn", "GAME"),
            ("spawn", "OVER"),
            ("spawn", "score"),
        ],
        "next_scene": {
            "end_scene": 'intro',
        }
    }
    return scene
