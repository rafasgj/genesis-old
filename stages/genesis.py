"""Game configuration"""

from engine import PropertyReference, GameVariable

Genesis = {
    "fps": 60,
    "window": {
        "size": "minimum",
        "minimum": (1024, 768),
        "maximum": (1920, 1080),
        "fullscreen": False
    },
    "variables": {
        "score": {
            "value": 0,
            "bind": [
                ("after", "ufo", "die", "add", 50)
            ]
        },
        "highscore": {
            "value": 0,
            "bind": [
                ("after", GameVariable("score"), "add",
                 "max", PropertyReference("score", "value"))
            ]
        },
        "lives": {
            "value": 3,
            "notifications": [
                ("after", "player", "die", "sub", 1)
            ]
        }
    },
    "fonts": {
        "genesis": {
            "filename": "media/fonts/open-24-display-st.ttf",
            "sizes": {
                "huge": 300,
                "large": 256,
                "normal": 64,
            }
        },
        "military": {
            "filename": "media/fonts/wmmilitary1.ttf",
            "sizes": {
                "normal": 24
            }
        }
    }
}
