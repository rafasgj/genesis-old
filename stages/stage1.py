"""Define the first stage of the game."""

from config import config
from util.notifications import after

from engine.text import Font

import pygame

import genesis


def create_scene(game_config):
    """Return the scene configuration."""
    width, _ = canvas_size = game_config['canvas_size']
    scene = {
        "name": "stage1",
        "mixer": {
            "config": game_config['mixer_config'],
            "loops": {
                "background_music": 'media/sound/Androids.ogg',
                "player_shoot": 'media/sound/enemy-kill.ogg',
                "enemy_kill": 'media/sound/laser.ogg',
                "player_kill": 'media/sound/mortar.ogg',
            }
        },
        "objects": {
            "player": {
                "class": "objects.player.Player",
                "init": {
                    "position": (200, 400),
                    "controller": {
                        "class": "engine.controllers.KeyboardController",
                        "init": {
                            "directional": (pygame.K_UP, pygame.K_DOWN,
                                            pygame.K_LEFT, pygame.K_RIGHT)
                        },
                        "bind": {
                            "up": {
                                (pygame.K_UP, pygame.K_DOWN,
                                 pygame.K_LEFT, pygame.K_RIGHT): "player_move"
                            },
                            "down": {
                                (pygame.K_UP, pygame.K_DOWN,
                                 pygame.K_LEFT, pygame.K_RIGHT): "player_move"
                            }
                        }
                    },
                    "speed": config.player_speed,
                },
                "notification": [
                    ("die", after, genesis.player_dead)
                ],
                "bind": {
                    "down": {
                        (pygame.K_SPACE,): genesis.player_shoot
                    }
                }
            },
            "life_stamp": {
                "class": "objects.stamp.Stamp",
                "init": {
                    "font": Font("media/fonts/wmmilitary1.ttf", 24),
                    "text": "A"
                }
            },
            "score": game_config['score'],
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
                },
                "notification": [
                    ("die", after, genesis.update_score_enemy)
                ]
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
