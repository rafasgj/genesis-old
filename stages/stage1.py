"""Define the first stage of the game."""

from config import config
from util.notifications import after

from engine import (SceneBehavior, PropertyReference,
                    GameFont, TheGame, Direction)
from engine.functions import Command, RandomInt, Choice, Add

import pygame

import genesis


life_stamp_description = {
    "class": "objects.stamp.Stamp",
    "init": {
        "font": GameFont("military.normal"),
        "text": "A"
    }
}

projectile_description = {
    "class": "objects.projectile.Projectile",
    "init": {
        "creator": None,
        "color": (0, 255, 255),
        "origin": PropertyReference("player", "center"),
        "target": Command(Add, PropertyReference("player", "center"),
                          Direction.right)
    }
}


def create_scene(game_config):
    """Return the scene configuration."""
    width, _ = canvas_size = game_config['canvas_size']
    scene = {
        "name": "stage1",
        "audio": {
            "loops": {
                "background_music": 'media/sound/Androids.ogg',
                "player_shoot": 'media/sound/enemy-kill.ogg',
                "enemy_kill": 'media/sound/laser.ogg',
                "player_kill": 'media/sound/mortar.ogg',
            }
        },
        "behaviors": {
            "sin_controller": {
                "class": "engine.controllers.SinController",
                "init": {
                    "length": width,
                    "freq": 1,
                    "amp": 1,
                    "speed": 1,
                    "vertical": False
                }
            },
            "const_controller": {
                "class": "engine.controllers.ConstantController",
                "init": {"dx": RandomInt(4, 7), "dy": 0}
            },
            "keyboard": {
                "class": "engine.controllers.KeyboardController",
                "init": {
                    "game": TheGame(),
                    "handlers": {
                        "down": {
                            pygame.K_UP: {"dx": 0, "dy": -1},
                            pygame.K_DOWN: {"dx": 0, "dy": +1},
                            pygame.K_LEFT: {"dx": -1, "dy": 0},
                            pygame.K_RIGHT: {"dx": +1, "dy": 0}
                        },
                        "up": {
                            pygame.K_UP: {"dx": 0, "dy": +1},
                            pygame.K_DOWN: {"dx": 0, "dy": -1},
                            pygame.K_LEFT: {"dx": +1, "dy": 0},
                            pygame.K_RIGHT: {"dx": -1, "dy": 0}
                        }
                    }
                }
            }
        },
        "objects": {
            "player": {
                "class": "objects.player.Player",
                "init": {
                    "position": (200, 400),
                    "controller": SceneBehavior('keyboard'),
                    "speed": config.player_speed,
                },
                "notification": [
                    ("die", after, genesis.player_dead)
                ]
            },
            "life_stamp": life_stamp_description,
            "projectile": projectile_description,
            "background": {
                "class": "objects.starfield.Starfield",
                "init": {
                    "canvas_size": canvas_size,
                    "count": 300
                }
            },
            "ufo": {
                "class": "objects.enemy.Enemy",
                "init": {
                    "canvas": canvas_size,
                    "image": 'media/images/ufo_spin.gif',
                    "controller": SceneBehavior(Choice("sin_controller",
                                                       "const_controller"))
                },
                "notification": [
                    ("die", after, genesis.update_score_enemy)
                ]
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
            (0, 0, "music_start", "background_music"),
            (3000, 750, "spawn", "ufo"),
            (8000, 1000, "call", genesis.enemy_shoot)
        ],
        "before": [
            ("spawn", ["background", "player", "score", "life_stamp"]),
            ("object", "score", "restart_score"),
            ("object", "score", "toggle_score"),
            ("object", "player", "respawn"),
            ("object", "life_stamp", "stamp",
             [(280, 35), (360, 35), (440, 35)])
        ],
        "next_scene": {
            "game_over": 'game_over',
            "end_scene": 'game_over'
        }
    }
    return scene
