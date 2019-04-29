"""Define the first stage of the game."""

from config import config
from util.notifications import after

from engine import (SceneBehavior, PropertyReference, SceneEvent,
                    GameFont, TheGame, Direction, SceneObject, GameVariable)
from engine.functions import RandomInt, Choice, Random

import pygame

import genesis


def create_scene(game_config):
    """Return the scene configuration."""
    width, _ = canvas_size = game_config['canvas_size']
    scene = {
        "name": "stage1",
        "audio": {
            "background_music": {
                "filename": 'media/sound/Androids.ogg',
                "loop": True,
                "autostart": True
            },
            "player_shoot": {"filename": 'media/sound/enemy-kill.ogg'},
            "enemy_kill": {"filename": 'media/sound/laser.ogg'},
            "player_kill": {"filename": 'media/sound/mortar.ogg'},
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
            "slow_controller": {
                "class": "engine.controllers.ConstantController",
                "init": {"dx": RandomInt(1, 3), "dy": 0}
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
                            pygame.K_RIGHT: {"dx": +1, "dy": 0},
                            pygame.K_SPACE: SceneEvent("spawn", "projectile"),
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
                    "speed": config.player_speed
                },
                "notifications": [
                    ("die", after, genesis.player_dead)
                ]
            },
            "life_stamp": {
                "class": "objects.stamp.Stamp",
                "init": {
                    "font": GameFont("military.normal"),
                    "text": "A"
                }
            },
            "projectile": {
                "class": "objects.projectile.Projectile",
                "init": {
                    "creator": SceneObject("player"),
                    "color": (255, 0, 255),
                    "origin": PropertyReference("player", "center"),
                    "direction": Direction.right,
                    "size": 12
                }
            },
            "background": {
                "class": "objects.starfield.Starfield",
                "init": {
                    "canvas_size": canvas_size,
                    "count": 300
                }
            },
            "ufo": {
                "class": "objects.enemy.KillableEnemy",
                "init": {
                    "canvas": canvas_size,
                    "image": 'media/images/ufo_spin.gif',
                    "controller": SceneBehavior(Choice("sin_controller",
                                                       "const_controller")),
                    "animate": True,
                    "bounding_shape": "ellipse"
                }
            },
            "asteroid": {
                "class": "objects.enemy.Enemy",
                "init": {
                    "canvas": canvas_size,
                    "image": 'media/images/asteroid.png',
                    "controller": SceneBehavior("slow_controller"),
                    "scale": Random(0.2, 0.75),
                    "bounding_shape": "ellipse"
                }
            },
            "score": {
                "class": "objects.score.Score",
                "init": {
                    "font": GameFont("genesis.normal"),
                    "position": (20, 5),
                    "animate": "True"
                },
                "bind": [
                    ("after", GameVariable('score'), "add",
                     "update_score", GameVariable('score'))
                ]
            }
        },
        "events": [
            (0, 0, "play_audio", "background_music"),
            (3000, 750, "spawn", "ufo"),
            (2000, 5000, "spawn", "asteroid"),
            (8000, 1000, "call", genesis.enemy_shoot)
        ],
        "before": [
            ("spawn", ["background", "player", "score", "life_stamp"]),
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
