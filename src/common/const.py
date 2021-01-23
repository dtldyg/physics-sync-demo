# coding=utf-8

# Game
CLIENT_FPS = 120
SERVER_FPS = 10
IO_FPS = 10
FPS_COLOR = (0, 255, 0, 255)  # green
SCREEN_SIZE = (400, 400)
SCREEN_BACKGROUND = (0, 0, 0, 255)  # black
# World
WORLD_G = 1  # const
# Entity
ENTITY_RADIUS = 20
ENTITY_MASS = 1  # const
ENTITY_FRICTION = 400
ENTITY_FORCE = 1200
ENTITY_MAX_V = 400

MASTER_INIT_POS = (50, SCREEN_SIZE[1] / 2)
MASTER_COLOR = (255, 0, 0, 255)  # red
MASTER_SHADOW_COLOR = (255, 0, 0, 127)  # red-half
REPLICA_INIT_POS = (SCREEN_SIZE[0] - MASTER_INIT_POS[0], SCREEN_SIZE[1] / 2)
REPLICA_COLOR = (255, 255, 0, 255)  # yellow
REPLICA_SHADOW_COLOR = (255, 255, 0, 127)  # yellow-half
