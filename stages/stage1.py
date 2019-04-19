"""Define the first stage of the game."""


def create_scene(globals):
    """Return the scene configuration."""
    width, _ = canvas_size = globals['canvas_size']
    stage_1 = {
        "mixer": {
            "config": globals['mixer_config'],
            "loops": {
                "background_music": 'media/sound/Androids.ogg',
                "player_shoot": 'media/sound/laser.ogg'
            }
        },
        "objects": {
            "player": globals['player'],
            "projectile": {
                "class": "objects.projectile.Projectile",
                "init": {
                    "creator": None,
                    "color": (0, 255, 255),
                    "origin": (0, 0, 0),
                    "target": (0, 0, 0)
                }
            },
            "background": {  # starfield
                "class": "objects.starfield.Starfield",
                "init": {"size": canvas_size}
            },
            "ufo": {
                "class": "objects.enemy.Enemy",
                "init": {
                    "canvas": canvas_size,
                    "image": 'media/images/ufo_spin.gif',
                    "controller": {
                        "class": "engine.controllers.SinController",
                        "init": {
                            "length": width,
                            "freq": 1,
                            "amp": 1,
                            "speed": 1,
                            "vertical": False
                        }
                    }
                }
            }
        },
        "events": [
            (0, 0, "music_start", "background_music"),
            (3000, 750, "spawn", "ufo"),
        ],
        "before": [
            ("spawn", "background"),
            ("spawn", "player")
        ]
    }
    return stage_1
