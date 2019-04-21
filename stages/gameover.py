"""Define the end screen."""

from engine import Font


def create_scene(game_config):
    """Return the scene configuration."""
    width, height = canvas_size = game_config['canvas_size']
    scene = {
        "name": "game_over",
        "mixer": {
            "config": game_config['mixer_config'],
            "loops": {
                "background_music": 'media/sound/Androids.ogg',
            }
        },
        "objects": {
            "background": {  # starfield
                "class": "objects.starfield.Starfield",
                "init": {"size": canvas_size}
            },
            "GAME": {
                "class": "engine.text.Label",
                "init": {
                    "font": Font('media/fonts/open-24-display-st.ttf', 300),
                    "text": "GAME",
                    "position": (0, 0, width, height // 2),
                    "centered": True
                }
            },
            "OVER": {
                "class": "engine.text.Label",
                "init": {
                    "font": Font('media/fonts/open-24-display-st.ttf', 300),
                    "text": "OVER",
                    "position": (0, height // 2, width, height),
                    "centered": True
                }
            },
            "score": game_config['score']
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
